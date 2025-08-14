import spacy
import subprocess
import sys

def get_model_by_language(language):
    # Map language code to spaCy model name
    mapping = {
        "en": "en_core_web_sm",
        "ru": "ru_core_news_sm",
        "de": "de_core_news_sm",
        "es": "es_core_news_sm",
        "fr": "fr_core_news_sm",
        # Add more as needed
    }
    return mapping.get(language)

def is_model_installed(model_name):
    try:
        spacy.util.get_package_path(model_name)
        return True
    except (OSError, ImportError):
        return False

def load_model(language_code):
    model_name = get_model_by_language(language_code)
    if not model_name:
        raise ValueError(f"No spaCy model found for language code '{language_code}'")
    if not is_model_installed(model_name):
        print(f"Model '{model_name}' not installed. Downloading...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
    return spacy.load(model_name)

def extract_lexeme_and_variant(token):
    # Returns (lexeme, variant)
    return (token.lemma_.lower(), token.text.lower())
