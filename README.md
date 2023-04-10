# Lexfreak
A language learner helper. Lexfreak will count the frequency of _lexemes_ (words, but ignoring inflections like plurals, verb tenses, etc.) in texts you read so you can prioritize what words you will learn by how much frequent you read them.

## The algorithm
The main algorithm is broken in two parts:

### Database
- Create a database with two tables:
   -  the main one has lexemes, frequency count, and a boolean if the word is already learned or not
   -  the secondary table has all the variants (actual words) instead of lexemes, in case you need to learn those too

### Handling new texts
-  Parse a text and, for each word:
   -  Grab its lexeme
   -  Check the database tables to see if the lexeme and word are already there, for each:
      - If it is, increase the the count
      - If it isn't, create a new entry

### Handling words/lexemes
- Show lexemes and words ordered by frequency
- Return or omit lexemes and words based on they being already learned

## Databases
Lexfreak adds the word counting in a database, but it tries to be engine agnostic. The first iteration will use [sqlite3](https://sqlite.org/index.html), just because it's... light. But other engines can be used by creating a module and a different values for the `--database-engine` flag.

## Natural Language Processing (NLP)
Lexfreak will also be NLP-library agnostic, but the first iteration will use [spaCy](https://spacy.io/)

## Flashcard apps
Since lexfreak helps prioritizing the words you want to learn, you can send its output to your favorite _flashcard_ (aka spaced repetition memorization) app. This will be a separate repo, though, since the idea is to be able to use lexfreak as a standalone tool, if you want

## Web app
As a quality of life, there will also be a web app that will use lexfreak as the backend tool. In the web app you can send the text for lexeme counting, have better visualization of your words, send the words to any supported flashcard app, etc. This will also be a separate repo.

# Other stuff
- Check the [TODO.md](/TODO.md) file for future plans
- Lexfreak is lincesed under [GPLv3](/LICENSE.md), and it's just a hobby project.