import sqlite3
from datetime import date
today = date.today()

def createTables(db):
	createWordsTable = """
		CREATE TABLE IF NOT EXISTS words(
			word TEXT PRIMARY KEY,
			freq INTEGER,
			studied INTEGER,
			added_on TEXT
		);
	"""
	
createVariantsTable = """
	CREATE TABLE IF NOT EXISTS variants(
		variant TEXT PRIMARY KEY,
		lexem TEXT,
		freq INTEGER,
		studied INTEGER,
		added_on TEXT
	);
	"""
saveFile = ".save" + file
db.execute(createWordsTable)
db.execute(createVariantsTable)
db.execute(saveFile)
return True

def connect(file):
	return sqlite3.connect(file)

def lemmaQuery(db,lemma):
	lemmaQuery = "SELECT * FROM words WHERE word = '" + lemma + "'"
	return db.execute(lemmaQuery).fetchone()

def variantQuery(db,variant):	
	variantQuery = "SELECT * FROM variants WHERE variant = '" + variant + "'"
	return db.execute(variantQuery).fetchone()

def insertWord(word,db):
	insertCommand = "".join([
		"INSERT INTO words ",
		"(word,freq,studied,added_on) ",
		"VALUES ('",
		word,
		"', ",
		"1, ",
		"FALSE, '",
		today.strftime("%Y-%m-%d"),
		"')"])
	db.execute(insertCommand)
	return True
	
def updateWord(word,freq,db):
		freq = lemmaResult[1] + 1 # TODO: update to query word and get word freq
		insertCommand = " ".join([
			"UPDATE words",
			"SET freq =",
			str(freq),
			"WHERE",
			"word =",
			"'" + token.lemma_ + "'"
		])
	db.execute(insertCommand)


	if(variantResult == None):
		variantInsertCommand = " ".join([
			"INSERT INTO variants",
			"(variant,lexem,freq,studied,added_on)",
			"VALUES",
			"('" + token.text.lower() + "',",
			"'" + token.lemma_ + "',",
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
			"'" + token.text.lower() + "'"
		])
	db.execute(variantInsertCommand)
	db.commit()