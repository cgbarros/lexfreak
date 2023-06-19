# user needs to choose model language 

# i made a prototype for the choosing language function, its commented below
# def whatlanguage(str):
#   import spacy
#   nlp = spacy.load(str + "_core_news_sm")



#import spacy
import spacy
nlp = spacy.load("pt_core_news_sm")

#function getLexemes
def getLexemes(txt):
  renderedText = nlp(txt)
  lexemeList = []
  for token in renderedText:
    if token.is_alpha:
      lexemeList.append(token.lemma_)
  return(lexemeList)


#merge with gitHub

