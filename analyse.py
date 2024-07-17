import pandas as pd
import os

from analysis.preprocess import clean_html, preprocess_text
from analysis.vader_analysis import get_vader_score
from analysis.textblob_analysis import get_textblob_score
# from analysis.spacy_analysis import get_spacy_score


def get_score(content, method='vader'):
    """
    Get sentiment score using the specified method.
    """
    if method == 'vader':
        return get_vader_score(content)
    elif method == 'textblob':
        return get_textblob_score(content)
    elif method == 'spacy':
        # return get_spacy_score(content)
        return 0
    else:
        raise ValueError("Unsupported method. Choose from 'vader', 'textblob', or 'spacy'.")


def describe_sentiment(term, posts):
    total_posts = len(posts)
    mean_sentiment = posts['sentiment'].mean()

    positive_posts = len(posts[posts['sentiment'] > 0.05])
    neutral_posts = len(posts[(posts['sentiment'] >= -0.05) & (posts['sentiment'] <= 0.05)])
    negative_posts = len(posts[posts['sentiment'] < -0.05])

    most_positive_post = posts.loc[posts['sentiment'].idxmax()]['content']
    most_negative_post = posts.loc[posts['sentiment'].idxmin()]['content']

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


def analyse_data(terms, input_dir, method='textblob'):
    print("Starting sentiment analysis")
    for term in terms:
        print(f"Analysing data for term: {term}")
        posts = pd.read_csv(os.path.join(input_dir, f'{term}_posts.csv'))

        # Clean and preprocess text
        posts['cleaned_content'] = posts['content'].apply(lambda x: clean_html(x)).apply(lambda x: preprocess_text(x))

        # Sentiment analysis on original and cleaned text
        posts['precleaned_sentiment'] = posts['content'].apply(lambda x: get_score(x, method=method))
        posts['sentiment'] = posts['cleaned_content'].apply(lambda x: get_score(x, method=method))

        # Save the results to CSV
        posts.to_csv(os.path.join(input_dir, f'{term}_posts_analysed.csv'), index=False)
        print(f"Saved analysed data for term: {term} to {input_dir}")

    sentiment_summary(terms, input_dir, input_dir)
    print("Sentiment analysis and summary completed")


if __name__ == "__main__":
    sample = ("It's curious, isn't it, how much Trump grasps at being respected, "
              "how much he plays up people calling him sir and such, while at the same time "
              "having absolutely no clue how respect is earned. The man wouldn't know integrity if it bit him on his "
              "239 pound ass."
              "Not even MAGA respects him; he's just their favorite bully. Not even my hubby, who voted for Trump "
              "twice and is probably poised to go again, " "would give a clear answer to the question Do you respect "
              "Donald Trump? The best Trump can hope to inspire in others is fear, not respect. " "And that's "
              "pathetic, considering the myriad advantages he's enjoyed in life.")

    use_method = 'vader'
    result = get_score(sample, method='textblob')
    print(f"Sentiment score for the input text using {use_method}: {result}")
