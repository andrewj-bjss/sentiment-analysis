import argparse

from mastodonFetch import check_stream_health
from retrieve import retrieve_data
from analyse import analyse_data
from trend_analysis import generate_trend_analysis
from visualise import plot_sentiment_distribution
from utils import get_latest_run_dir


def main():
    parser = argparse.ArgumentParser(description='Sentiment Analysis Pipeline')
    parser.add_argument('--source', choices=['mastodon', 'bluesky', 'all'], default='mastodon',
                        help='Source to retrieve from')
    parser.add_argument('--fetch-behaviour', choices=['reuse-last', 'always-fetch', 'last-run-or-error',
                        'specified-run-or-error'], default='reuse-last', help='Data fetching behaviour')
    parser.add_argument('--output-dir', type=str, default='output', help='Output directory')
    parser.add_argument('--terms', nargs='+', required=True,
                        help='Terms for analysis (space-separated list for multiple terms)')
    parser.add_argument('--mode', choices=['fetch', 'fetch-analyse', 'analyse-visualise', 'visualise',
                        'trend-analysis', 'full-analysis'], default='fetch-analyse-visualise', help='Operation mode')
    parser.add_argument('--resample-period', type=str, default='H',
                        help='Resampling period for trend analysis (e.g., H for hourly, D for daily)')

    args = parser.parse_args()

    check_stream_health()

    output_dir = None
    if args.mode in ['fetch', 'fetch-analyse', 'fetch-analyse-visualise', 'full-analysis']:
        output_dir = retrieve_data(args.terms, args.source, args.fetch_behaviour, args.output_dir)

    if args.mode in ['fetch-analyse', 'analyse-visualise', 'fetch-analyse-visualise', 'full-analysis']:
        if not output_dir:
            output_dir = get_latest_run_dir(base_dir=args.output_dir)
            if not output_dir:
                print("No previous run found and no retrieval specified. Exiting.")
                return
        analyse_data(args.terms, output_dir)

    if args.mode in ['analyse-visualise', 'visualise', 'fetch-analyse-visualise', 'full-analysis']:
        if not output_dir:
            output_dir = get_latest_run_dir(base_dir=args.output_dir)
            if not output_dir:
                print("No previous run found and no retrieval specified. Exiting.")
                return
        plot_sentiment_distribution(args.terms, output_dir)

    if args.mode in ['trend-analysis', 'full-analysis']:
        generate_trend_analysis(args.output_dir, args.terms, args.resample_period)


if __name__ == '__main__':
    main()
