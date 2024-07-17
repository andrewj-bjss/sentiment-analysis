import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import os

matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive plotting


def plot_sentiment_distribution(terms, input_dir):
    plt.figure(figsize=(12, 6))
    colors = ['blue', 'red', 'green', 'purple', 'orange']

    for i, term in enumerate(terms):
        print(f"Visualizing data for term: {term}")
        posts = pd.read_csv(os.path.join(input_dir, f'{term}_posts_analysed.csv'))
        plt.hist(posts['sentiment'], bins=20, alpha=0.5, label=term, color=colors[i % len(colors)])

    plt.xlabel('Sentiment Score')
    plt.ylabel('Number of Posts')
    plt.title('Sentiment Analysis of Terms')
    plt.xticks([-1, -0.5, 0, 0.5, 1], ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive'])
    plt.legend(loc='upper right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    output_file = os.path.join(input_dir, 'sentiment_distribution.png')
    plt.savefig(output_file)
    plt.close()  # Close the plot to free up memory
    print(f"Visualization saved to {output_file}")


# Example usage
# input_dir = 'output/latest_run'
# terms = ['Biden', 'Trump']
# plot_sentiment_distribution(terms, input_dir)
