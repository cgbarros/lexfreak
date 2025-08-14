import argparse
import os
import uuid
import module_translator

# Set functions according to selected engines 
## Main procedures

def count(args):
    title = args.title if args.title else args.input
    url = args.url if args.url else args.input
    reference_id = str(uuid.uuid4())

    print(f"Loading modules '{args.db_engine}' and '{args.nlp_engine}'")
    
    (
      db,
      create_tables,
      upsert_reference,
      upsert_lexeme,
      upsert_variant,
      link_reference_variant_lexeme,
      close_connection,
      nlp,
      extract_lexeme_and_variant
    ) = module_translator.set_count_functions(args.db_engine, args.nlp_engine, args.language)

    print("Modules loaded. Connecting to the database.")
    create_tables(db)

    print(f"Upserting reference {title}")
    upsert_reference(db, reference_id, title, args.author, url, args.language)

    # print("[DEBUG] testing the tables")
    # cursor = db.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # tables = cursor.fetchall()

    # Getting the total number of lines

    with open(args.input, "r") as f:
        line_total = sum(1 for _ in f)

    with open(args.input, "r") as f:
        line_counter = 0
        for line in f:
            line_counter += 1
            print(f"Processing line {line_counter} of {line_total}")
            tokens = nlp(line)
            for token in tokens:
                extracted_props = extract_lexeme_and_variant(token)
                if not extracted_props:
                    continue
                lexeme, variant = extracted_props
                upsert_lexeme(db, lexeme, args.language)
                upsert_variant(db, variant, lexeme, args.language)
                link_reference_variant_lexeme(db, reference_id, variant, lexeme, args.language)
    
    close_connection(db)
    print("Done!")

def show(args):
    (
      db,
      get_reference_by_title,
      get_reference_by_url,
      get_lexemes,
      get_variants
    ) = module_translator.set_show_functions(args.db_engine)
    # Only one of --title, --url, --ref-id allowed
    ref_args = [args.title, args.url, args.ref_id]
    if sum(x is not None for x in ref_args) > 1:
        raise ValueError("Only one of --title, --url, or --ref-id may be specified.")

    if args.title:
        reference_id = get_reference_by_title(db, args.title)
    elif args.url:
        reference_id = get_reference_by_url(db, args.url)
    elif args.ref_id:
        reference_id = args.ref_id

    max_results = args.max_results

    if args.command == "lexemes":
        results = get_lexemes(db, reference_id, max_results, args.language)
    elif args.command == "variants":
        results = get_variants(db, reference_id, max_results, args.language)
    else:
        raise ValueError("Unknown show command. Use 'lexemes' or 'variants'.")

    for word, freq in results:
        print(f"{word}\t{freq}")

    close_connection() 

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    count_parser = subparsers.add_parser("count")
    count_parser.add_argument("--input", required=True, help="Input file")
    count_parser.add_argument("--language", required=True, help="Language code (en, ru, de, etc.)")
    count_parser.add_argument("--title", help="Text title")
    count_parser.add_argument("--author", help="Text author")
    count_parser.add_argument("--url", help="Text URL or Path")
    count_parser.add_argument("--db-engine", default="sqlite", help="Database engine (default: sqlite)")
    count_parser.add_argument("--nlp-engine", default="spacy", help="NLP engine (default: spacy)")

    # Show command with subcommands
    show_parser = subparsers.add_parser("show")
    show_subparsers = show_parser.add_subparsers(dest="show_command", required=True)

    # Show commands: lexemes and variants
    for show_cmd in ["lexemes", "variants"]:
        show_parser = subparsers.add_parser(show_cmd)
        show_parser.add_argument("--database", required=True, help="Database file")
        show_parser.add_argument("--db-engine", default="sqlite", help="Database engine (default: sqlite)")
        show_parser.add_argument("--language", help="Language code (en, ru, de, etc.)")
        group = show_parser.add_mutually_exclusive_group()
        group.add_argument("--title", help="Reference title")
        group.add_argument("--url", help="Reference URL")
        group.add_argument("--ref-id", help="Reference ID")
        show_parser.add_argument("--max-results", type=int, help="Maximum number of results")

    args = parser.parse_args()

    if args.command == "count":
        count(args)
    if args.command == "show":
        show(args)

if __name__ == "__main__":
    main()
