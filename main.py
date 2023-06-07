import spacy
import argparse

nlp = spacy.load("ru_core_news_lg")
parser = argparse.ArgumentParser()
installedModels = spacy.util.get_installed_models()

parser.add_argument("-i", "--input", help="Input file")
parser.add_argument("-m", "--model", help="Language model")
parser.add_argument("-sM", "--show-models", help="Show installed models")
parser.add_argument("-gM", "--get-model", help="Install model")
parser.add_argument("-rM", "--remove-model", help="Uninstall model")
parser.add_argument("-db", "--database", help="Database file")
parser.add_argument("-dbE", "--database-engine", help="Database engine")

txtFile = open("new_text.txt")
txtStr = txtFile.read()
txtFile.close()

txt = nlp(txtStr)

for token in txt:
	if (token.is_alpha):
		updateDb(token, db)

print("done")
