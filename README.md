# Sentiment Analysis Pipeline

This project provides a comprehensive sentiment analysis pipeline that fetches data from Mastodon, analyses sentiment, generates descriptive summaries, and visualises the results. It also supports generating trend visualisations based on historical data.

## Features

- Fetch data from Mastodon or BlueSky (support for BlueSky to be added).
- Analyse sentiment using VADER Sentiment Analyzer.
- Generate descriptive summaries of sentiment data.
- Visualise sentiment distributions.
- Generate trend visualisations based on historical data.

## Installation

### Prerequisites

- Python 3.8 or higher
- Pip (Python package installer)

### Install Dependencies

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/sentiment-analysis-pipeline.git
   cd sentiment-analysis-pipeline

2. Install the required Python packages:

   ```sh
   pip install -r requirements.txt

### Environment Variables
Create a .env file in the root directory of the project and add your Mastodon credentials:

```
MASTODON_CLIENT_ID=your_client_id
MASTODON_CLIENT_SECRET=your_client_secret
MASTODON_ACCESS_TOKEN=your_access_token
MASTODON_API_BASE_URL=https://mastodon.social
```

## Usage

### Command Line Interface
The main.py script is the entry point for the pipeline. It accepts various parameters to control its behaviour.

### Parameters
- --terms: Terms for analysis (space-separated list for multiple terms). Required.
- --source: Source to retrieve data from (mastodon, bluesky, all). Default is mastodon.
- --fetch-behaviour: Behaviour for fetching data:
  - reuse-last: Reuse the last run's data if available; otherwise, fetch new data.
  - always-fetch: Always fetch new data from the API.
  - last-run-or-error: Use the last run's data or exit with an error if no previous data is available.
  - specified-run-or-error: Use specified run's data or exit with an error if not available.
- --output-dir: Directory to save output files. Default is ```output```.
- --mode: Operation mode:
  - fetch: Just fetch and store data.
  - fetch-analyse: Fetch and analyse data.
  - analyse-visualise: Re-analyse last fetched run and visualise.
  - visualise: Visualise last analysed run.
  - trend-analysis: Generate trend visualisations based on all runs.
  - full-analysis: Fetch new data, analyse, summarise, and generate all visualisations.
- --resample-period: Resampling period for trend analysis (e.g., H for hourly, D for daily). Default is H.

### Example Commands

Fetch new data, analyze, and generate all visualisations:

```sh
python main.py --terms "Biden" "Trump" --fetch-behaviour always-fetch --mode full-analysis --resample-period H
```

Reuse last run's data, analyse, and visualise:

```sh
python main.py --terms "Biden" "Trump" --fetch-behaviour reuse-last --mode analyse-visualise
```
Generate trend visualisations based on all runs:

```sh
python main.py --terms "Biden" "Trump" --mode trend-analysis --resample-period D
```

## Project Structure
- main.py: Main entry point for the pipeline.
- retrieve.py: Functions for fetching data from sources.
- analyse.py: Functions for analyzing sentiment and generating summaries.
- visualise.py: Functions for visualizing sentiment distributions.
- trend_analysis.py: Functions for generating trend visualizations.
- utils.py: Utility functions for managing output directories.
