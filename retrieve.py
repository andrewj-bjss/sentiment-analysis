import os
from mastodonFetch import fetch_posts
from utils import create_output_dir, get_latest_run_dir


def retrieve_terms(terms, output_dir, source='mastodon'):
    for term in terms:
        print(f"Retrieving data for term: {term}")
        if source == 'mastodon':
            posts = fetch_posts(term, 1000)
            posts.to_csv(os.path.join(output_dir, f'{term}_posts.csv'), index=False)
            print(f"Saved posts for term: {term} to {output_dir}")
        # Add elif block for other sources (like BlueSky) here


def retrieve_data(terms, source='mastodon', fetch_behaviour='reuse-last', output_dir='output'):
    if output_dir is None:
        output_dir = 'output'
    if fetch_behaviour in ['always-fetch', 'specified-run-or-error']:
        output_dir = create_output_dir(base_dir=output_dir)
        retrieve_terms(terms, output_dir, source)
    elif fetch_behaviour == 'reuse-last':
        output_dir = get_latest_run_dir(base_dir=output_dir)
        if not output_dir:
            print("No previous run found. Fetching new data from the API.")
            output_dir = create_output_dir(base_dir=output_dir)
            retrieve_terms(terms, output_dir, source)
        else:
            print(f"Reusing data from the last run: {output_dir}")
    elif fetch_behaviour == 'last-run-or-error':
        output_dir = get_latest_run_dir(base_dir=output_dir)
        if not output_dir:
            raise FileNotFoundError('No previous run found. Please fetch data first.')
    return output_dir
