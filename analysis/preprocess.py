import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK datasets
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def clean_html(raw_html):
    """
    Clean and strip HTML tags from the given text.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()


def preprocess_text(text):
    """
    Preprocess the text by tokenizing, removing stopwords, and lemmatizing.
    """
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.lower() not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)
