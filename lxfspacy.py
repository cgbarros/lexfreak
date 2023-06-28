import spacy

language_dict = {
  "pt": {
    "speed": "pt_core_news_sm",
    "accuracy": "pt_core_news_lg"
  },
  "en": {
   "speed": "en_core_web_sm",
   "accuracy": "en_core_web_trf"
  },
  "ru": {
    "speed": "ru_core_news_sm",
    "accuracy": "ru_core_news_lg"
  }
}
 
def nlp(lang, opt):
  return spacy.load(language_dict[lang][opt])

#function getLexemes
def getLexemes(txt, nlp):
  renderedText = nlp(txt)
  lexemeList = []
  for token in renderedText:
    if token.is_alpha:
      lexemeList.append(token.lemma_)
  return(lexemeList)

