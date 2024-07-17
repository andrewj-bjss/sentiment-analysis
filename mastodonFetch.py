from mastodon import Mastodon
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv('.env.local'))
load_dotenv(find_dotenv('.env'))

# Initialize Mastodon
mastodon = Mastodon(
    client_id=os.getenv('MASTODON_CLIENT_ID'),
    client_secret=os.getenv('MASTODON_CLIENT_SECRET'),
    access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
    api_base_url=os.getenv('MASTODON_API_BASE_URL')
)


def fetch_posts(query, limit=100):
    print(f"Fetching posts for query: {query}")
    statuses = mastodon.timeline_hashtag(query, limit=limit)
    posts = [{'id': status['id'], 'content': status['content'], 'created_at': status['created_at'], 'source': 'mastodon'
              } for status in statuses]
    print(f"Fetched {len(posts)} posts for query: {query}")
    return pd.DataFrame(posts)
