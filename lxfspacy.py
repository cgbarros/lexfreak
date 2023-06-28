# user needs to choose model language 


import spacy 

def nlp(str):
  return spacy.load(str)

#function getLexemes
def getLexemes(txt):
  renderedText = nlp(txt)
  lexemeList = []
  for token in renderedText:
    if token.is_alpha:
      lexemeList.append(token.lemma_)
  return(lexemeList)



