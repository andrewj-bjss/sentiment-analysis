from textblob import TextBlob
from analysis.preprocess import clean_html, preprocess_text


def get_textblob_score(content):
    """
    Get sentiment score using TextBlob.
    """
    cleaned_content = preprocess_text(clean_html(content))
    blob = TextBlob(cleaned_content)
    score = blob.sentiment.polarity
    return score
