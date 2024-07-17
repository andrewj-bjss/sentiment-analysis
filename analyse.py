import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
import nltk
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


def describe_sentiment(term, posts):
    total_posts = len(posts)
    mean_sentiment = posts['sentiment'].mean()

    positive_posts = len(posts[posts['sentiment'] > 0.05])
    neutral_posts = len(posts[(posts['sentiment'] >= -0.05) & (posts['sentiment'] <= 0.05)])
    negative_posts = len(posts[posts['sentiment'] < -0.05])

    most_positive_post = clean_html(posts.loc[posts['sentiment'].idxmax()]['content'])
    most_negative_post = clean_html(posts.loc[posts['sentiment'].idxmin()]['content'])

    summary = f"""
    Sentiment Summary for '{term}':
    -------------------------------
    Total Posts: {total_posts}
    Average Sentiment Score: {mean_sentiment:.2f}

    Sentiment Distribution:
      Positive: {positive_posts} ({positive_posts / total_posts:.2%})
      Neutral: {neutral_posts} ({neutral_posts / total_posts:.2%})
      Negative: {negative_posts} ({negative_posts / total_posts:.2%})

    Most Positive Post:
    {most_positive_post}

    Most Negative Post:
    {most_negative_post}
    """

    return summary, positive_posts, total_posts


def sentiment_summary(terms, input_dir, output_dir):
    summaries = []
    term_data = {}

    for term in terms:
        posts = pd.read_csv(os.path.join(input_dir, f'{term}_posts_analysed.csv'))
        summary, positive_posts, total_posts = describe_sentiment(term, posts)
        summaries.append(summary)
        term_data[term] = (positive_posts, total_posts)

    # Comparative summary
    term1, term2 = terms
    term1_positive, term1_total = term_data[term1]
    term2_positive, term2_total = term_data[term2]

    term1_ratio = term1_positive / term1_total
    term2_ratio = term2_positive / term2_total

    if term1_ratio > term2_ratio:
        support_ratio = term1_ratio / term2_ratio
        support_summary = (f"Overall, {term1} is receiving more support than {term2}, with a support ratio of "
                           f"approximately {support_ratio:.2f} to 1.")
    else:
        support_ratio = term2_ratio / term1_ratio
        support_summary = (f"Overall, {term2} is receiving more support than {term1}, with a support ratio of "
                           f"approximately {support_ratio:.2f} to 1.")

    summaries.append(support_summary)

    # Save summaries to a text file
    summary_file = os.path.join(output_dir, 'sentiment_summary.txt')
    with open(summary_file, 'w') as f:
        for summary in summaries:
            f.write(summary)
            f.write('\n\n')
    print(f"Sentiment summaries saved to {summary_file}")


def analyse_data(terms, input_dir):
    print("Starting sentiment analysis")
    analyzer = SentimentIntensityAnalyzer()
    for term in terms:
        print(f"Analysing data for term: {term}")
        posts = pd.read_csv(os.path.join(input_dir, f'{term}_posts.csv'))

        # Clean and preprocess text
        posts['cleaned_content'] = posts['content'].apply(clean_html).apply(preprocess_text)

        # Sentiment analysis on original and cleaned text
        posts['precleaned_sentiment'] = posts['content'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
        posts['sentiment'] = posts['cleaned_content'].apply(lambda x: analyzer.polarity_scores(x)['compound'])

        # Save the results to CSV
        posts.to_csv(os.path.join(input_dir, f'{term}_posts_analysed.csv'), index=False)
        print(f"Saved analysed data for term: {term} to {input_dir}")

    sentiment_summary(terms, input_dir, input_dir)
    print("Sentiment analysis and summary completed")
