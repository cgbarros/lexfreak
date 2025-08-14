import sqlite3
from datetime import date

# General functions

def connect(file):
	return sqlite3.connect(file)

def close_connection(conn):
    conn.close()

# COUNT command functions

def create_tables(db):
    createLexemesTable = """
        CREATE TABLE IF NOT EXISTS lexemes(
            lexeme TEXT PRIMARY KEY,
            language TEXT,
            freq INTEGER,
            added_on TEXT
        );
    """

    createVariantsTable = """
        CREATE TABLE IF NOT EXISTS variants(
            variant TEXT PRIMARY KEY,
            lexeme TEXT,
            language TEXT,
            freq INTEGER,
            added_on TEXT
        );
        """

    createReferencesTable = """
        CREATE TABLE IF NOT EXISTS refs(
            id TEXT PRIMARY KEY,
            title TEXT,
            author TEXT,
            url TEXT,
            language TEXT,
            added_on TEXT
        )
    """

    createReferenceVariantLexemeTable = """
        CREATE TABLE IF NOT EXISTS reference_variant_lexeme(
            reference_id TEXT,
            variant,
            lexeme,
            language
        )
    """

    db.execute(createLexemesTable)
    db.execute(createVariantsTable)
    db.execute(createReferencesTable)
    db.execute(createReferenceVariantLexemeTable)
    db.commit()
    return True

def upsert_lexeme(conn, lexeme, language):
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("SELECT freq FROM lexemes WHERE lexeme = ?", (lexeme,))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE lexemes SET freq = freq + 1 WHERE lexeme = ?", (lexeme,))
    else:
        cur.execute("INSERT INTO lexemes (lexeme, language, freq, added_on) VALUES (?, ?, ?, ?)", (lexeme, language, 1, today))
    conn.commit()

def upsert_variant(conn, variant, lexeme, language):
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("SELECT freq FROM variants WHERE variant = ?", (variant,))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE variants SET freq = freq + 1 WHERE variant = ?", (variant,))
    else:
        cur.execute("INSERT INTO variants (variant, lexeme, language, freq, added_on) VALUES (?, ?, ?, ?, ?)", (variant, lexeme, language, 1, today))
    conn.commit()

def upsert_reference(conn, reference_id, title, author, url, language):
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("INSERT OR IGNORE INTO refs (id, title, author, url, language, added_on) VALUES (?, ?, ?, ?, ?, ?)", (reference_id, title, author, url, language, today))
    conn.commit()

def link_reference_variant_lexeme(conn, reference_id, variant, lexeme, language):
    cur = conn.cursor()
    cur.execute("INSERT INTO reference_variant_lexeme (reference_id, variant, lexeme, language) VALUES (?, ?, ?, ?)", (reference_id, variant, lexeme, language))
    conn.commit()

# SHOW command functions

def get_reference_by_title(conn, title):
    cur = conn.cursor()
    cur.execute("SELECT id FROM refs WHERE title = ?", (title,))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        raise ValueError(f"Reference with title '{title}' not found.")

def get_reference_by_url(conn, url):
    cur = conn.cursor()
    cur.execute("SELECT id FROM refs WHERE url = ?", (url,))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        raise ValueError(f"Reference with url '{url}' not found.")

def get_lexemes(conn, reference_id=None, max_results=None, language=None):
    cur = conn.cursor()
    params = []
    query = """
        SELECT lexemes.lexeme, lexemes.freq
        FROM lexemes
    """
    where_clauses = []
    if reference_id:
        query += " JOIN reference_variant_lexeme ON lexemes.lexeme = reference_variant_lexeme.lexeme"
        where_clauses.append("reference_variant_lexeme.reference_id = ?")
        params.append(reference_id)
    if language:
        where_clauses.append("lexemes.language = ?")
        params.append(language)
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " GROUP BY lexemes.lexeme ORDER BY lexemes.freq DESC"
    if max_results:
        query += " LIMIT ?"
        params.append(max_results)
    cur.execute(query, tuple(params))
    return cur.fetchall()

def get_variants(conn, reference_id=None, max_results=None, language=None):
    cur = conn.cursor()
    params = []
    query = """
        SELECT variants.variant, variants.freq
        FROM variants
    """
    where_clauses = []
    if reference_id:
        query += " JOIN reference_variant_lexeme ON variants.variant = reference_variant_lexeme.variant"
        where_clauses.append("reference_variant_lexeme.reference_id = ?")
        params.append(reference_id)
    if language:
        where_clauses.append("variants.language = ?")
        params.append(language)
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    query += " GROUP BY variants.variant ORDER BY variants.freq DESC"
    if max_results:
        query += " LIMIT ?"
        params.append(max_results)
    cur.execute(query, tuple(params))
    return cur.fetchall()
