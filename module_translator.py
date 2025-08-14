def set_count_functions(db_engine, nlp_engine, language):
    if db_engine == "sqlite":
        import lxfsqlite
        db = lxfsqlite.connect("lexfreak.db")
        create_tables = lxfsqlite.create_tables
        upsert_reference = lxfsqlite.upsert_reference
        upsert_lexeme = lxfsqlite.upsert_lexeme
        upsert_variant = lxfsqlite.upsert_variant
        link_reference_variant_lexeme = lxfsqlite.link_reference_variant_lexeme
        close_connection = lxfsqlite.close_connection
    else:
        raise ValueError(f"Unsupported database engine: {db_engine}")

    if nlp_engine == "spacy":
        import lxfspacy
        nlp = lxfspacy.load_model(language)
        extract_lexeme_and_variant = lxfspacy.extract_lexeme_and_variant
    else:
        raise ValueError(f"Unsupported NLP engine: {nlp_engine}")

    return (
            db,
            create_tables,
            upsert_reference,
            upsert_lexeme,
            upsert_variant,
            link_reference_variant_lexeme,
            close_connection,
            nlp,
            extract_lexeme_and_variant
           )

def set_show_functions(db_engine):
    if db_engine == "sqlite":
        import lxfsqlite
        db = lxfsqlite.connect(args.database)
        get_reference_by_title = lxfsqlite.get_reference_by_title
        get_reference_by_url = lxfsqlite.get_reference_by_url
        get_lexemes = lxfsqlite.get_lexemes
        get_variants = lxfsqlite.get_variants
        close_connection = lxfsqlite.close_connection
    else:
        raise ValueError(f"Unsupported database engine: {db_engine}")

    return (
            db,
            get_reference_by_title,
            get_reference_by_url,
            get_lexemes,
            get_variants
           )
