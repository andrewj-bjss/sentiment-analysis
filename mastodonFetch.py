from mastodon import Mastodon
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os
import time

load_dotenv(find_dotenv('.env.local'))
load_dotenv(find_dotenv('.env'))

# Initialize Mastodon
mastodon = Mastodon(
    client_id=os.getenv('MASTODON_CLIENT_ID'),
    client_secret=os.getenv('MASTODON_CLIENT_SECRET'),
    access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
    api_base_url=os.getenv('MASTODON_API_BASE_URL')
)


def check_stream_health():
    """
    Check the health of the streaming API connection.
    """
    stream_health = mastodon.stream_healthy()
    if not stream_health:
        print("The streaming API connection is not healthy. Exiting application.")
        exit(1)
    print("The streaming API connection is healthy.")


def fetch_posts(query, total_limit=100):
    """
    Fetch posts for a given query from Mastodon, supporting pagination.
    """

    print(f"Fetching posts for query: {query}")
    all_posts = []
    limit_per_page = 40  # Mastodon's limit per request
    page_number = 1

    statuses = mastodon.timeline_hashtag(query, limit=limit_per_page)
    while statuses:
        print(f"Fetching page {page_number}")

        # Filter posts based on language
        posts = [
            {
                'id': status['id'],
                'content': status['content'],
                'created_at': status['created_at'],
                'language': status.get('language', ''),
                'source': 'mastodon'
            }
            for status in statuses
            if status.get('language') in ['en', '']
        ]
        all_posts.extend(posts)

        # Check if we've hit the total limit
        if len(all_posts) >= total_limit:
            break

        # Get the next page of results
        statuses = mastodon.fetch_next(statuses)

        # Respect rate limit
        # time.sleep(1)
        page_number += 1

    # Trim to the exact total limit if we exceeded
    all_posts = all_posts[:total_limit]

    print(f"Fetched {len(all_posts)} posts for query: {query}")
    return pd.DataFrame(all_posts)


# Example usage (if running this script directly)
if __name__ == "__main__":
    example_query = "example"
    posts_df = fetch_posts(example_query, total_limit=1000)
    posts_df.to_csv(f"{example_query}_posts.csv", index=False)
    print(f"Posts saved to {example_query}_posts.csv")
