import spacy
from analysis.preprocess import clean_html, preprocess_text

nlp = spacy.load("en_core_web_sm")


def get_spacy_score(content):
    """
    Get sentiment score using SpaCy.
    """
    cleaned_content = preprocess_text(clean_html(content))
    doc = nlp(cleaned_content)
    score = doc._.polarity
    return score
