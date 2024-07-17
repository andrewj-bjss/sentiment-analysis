from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from analysis.preprocess import clean_html, preprocess_text

analyzer = SentimentIntensityAnalyzer()


def get_vader_score(content):
    """
    Get sentiment score using VADER.
    """
    cleaned_content = preprocess_text(clean_html(content))
    score = analyzer.polarity_scores(cleaned_content)['compound']
    return score
