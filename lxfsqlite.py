import sqlite3
from datetime import date
today = date.today()

def createTables(db):
	createLexemesTable = """
		CREATE TABLE IF NOT EXISTS lexemes(
			lexeme TEXT PRIMARY KEY,
			freq INTEGER,
			studied INTEGER,
			added_on TEXT
		);
	"""
	createVariantsTable = """
		CREATE TABLE IF NOT EXISTS variants(
			variant TEXT PRIMARY KEY,
			lexeme TEXT,
			freq INTEGER,
			studied INTEGER,
			added_on TEXT
		);
		"""
	saveFile = ".save " + file
	db.execute(createLexemesTable)
	db.execute(createVariantsTable)
	db.execute(saveFile)
	return True

def connect(file):
	return sqlite3.connect(file)

def lexemeQuery(db,lexeme):
	lexemeQuery = "SELECT * FROM lexemes WHERE lexeme = '" + lexeme + "'"
	return db.execute(lexemeQuery).fetchone()

def variantQuery(db,variant):	
	variantQuery = "SELECT * FROM variants WHERE variant = '" + variant + "'"
	return db.execute(variantQuery).fetchone()

def insertLexeme(lexeme,db):
	insertCommand = "".join([
		"INSERT INTO lexemes ",
		"(lexeme,freq,studied,added_on) ",
		"VALUES ('",
		lexeme,
		"', ",
		"1, ",
		"FALSE, '",
		today.strftime("%Y-%m-%d"),
		"')"])
	db.execute(insertCommand)
	return True
	
def updateToken(lexeme,variant,freq,db):
	  lexemeResult = lexemeQuery(lexeme,db)
		freq = lexemeResult[1] + 1
		insertCommand = " ".join([
			"UPDATE lexemes",
			"SET freq =",
			str(freq),
			"WHERE",
			"lexeme =",
			"'" + lexeme + "'"
		])
	db.execute(insertCommand)

	if(variantResult == None):
		variantInsertCommand = " ".join([
			"INSERT INTO variants",
			"(variant,lexem,freq,studied,added_on)",
			"VALUES",
			"('" + variant.text.lower() + "',",
			"'" + lexem + "',",
			"1,"
			"FALSE,"
			"'" + today.strftime("%Y-%m-%d") + "')"
		])
	else:
		variantFreq = variantResult[2] + 1
		variantInsertCommand = " ".join([
			"UPDATE variants",
			"SET freq =",
			str(variantFreq),
			"WHERE",
			"variant =",
			"'" + variant.text.lower() + "'"
		])
	db.execute(variantInsertCommand)
	db.commit()