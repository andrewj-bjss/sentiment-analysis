import matplotlib
import os
import pandas as pd
import matplotlib.pyplot as plt

matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive plotting


def aggregate_sentiment_data(base_dir='output', terms=['Biden', 'Trump']):
    all_data = {term: [] for term in terms}
    for run_dir in os.listdir(base_dir):
        run_path = os.path.join(base_dir, run_dir)
        if os.path.isdir(run_path):
            for term in terms:
                file_path = os.path.join(run_path, f'{term}_posts_analysed.csv')
                if os.path.exists(file_path):
                    posts = pd.read_csv(file_path)
                    # Parse the datetime correctly
                    posts['created_at'] = pd.to_datetime(posts['created_at'], format='%Y-%m-%d %H:%M:%S%z', errors='coerce')
                    all_data[term].append(posts)

    aggregated_data = {term: pd.concat(data) for term, data in all_data.items()}
    return aggregated_data


def plot_historical_trends(aggregated_data, output_dir, resample_period='H'):
    plt.figure(figsize=(12, 6))
    for term, data in aggregated_data.items():
        print(f"Plotting data for term: {term}")
        data.set_index('created_at', inplace=True)
        sentiment_over_time = data['sentiment'].resample(resample_period).mean()
        plt.plot(sentiment_over_time, label=term)
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score')
    plt.title('Historical Sentiment Trends')
    plt.legend()
    output_file = os.path.join(output_dir, 'historical_sentiment_trends.png')
    plt.savefig(output_file)
    plt.close()  # Close the plot to free up memory
    print(f"Historical trend analysis saved to {output_file}")


def generate_trend_analysis(base_dir='output', terms=['Biden', 'Trump'], resample_period='H'):
    print("Aggregating sentiment data from all runs...")
    aggregated_data = aggregate_sentiment_data(base_dir, terms)
    print("Aggregated sentiment data.")
    plot_historical_trends(aggregated_data, base_dir, resample_period)
    print("Historical trend analysis completed")

# Example usage:
# generate_trend_analysis()
