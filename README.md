# SOEN321 YouTube Comment Link Analyzer

## What it does
- Searches YouTube for a list of Canadian subjects and collects top video links
- Pulls recent comments for each video and checks for links/domains
- Categorizes detected domains and saves everything to a CSV
- Provides a plotting script to visualize links and categories

## Requirements
- Python 3.10+
- YouTube Data API v3 key
- Packages: google-api-python-client, pandas, matplotlib, seaborn, joblib

Install the dependencies:
`
pip install google-api-python-client pandas matplotlib seaborn joblib
`

## Setup
1. Add your API key
   - Open search_and_analyse.py and anaylze_comments.py
   - Replace YOUTUBE_API_KEY = "api" with your key (use the same value in both files)
2. Optional tweaks
   - Edit SUBJECTS or VIDEOS_PER_SUBJECT in search_and_analyse.py to change what gets searched
   - Edit DEFAULT_MAX_COMMENTS in anaylze_comments.py to adjust how many comments are pulled per video (default 300)
   - Change RESULTS_CSV if you want the output file renamed or stored elsewhere

## Run: collect data
`
python search_and_analyse.py
`
- Saves video_link_results.csv in the project root
- Columns: CONTENT, HAS_LINK, LINK_DOMAIN, LINK_CATEGORY, subject, video_url

## Run: plot results
`
python plotter.py
`
- Expects video_link_results.csv
- Shows bar charts for link vs no-link, link categories, top domains, per-subject counts, and per-video counts

## Notes
- Fetching comments consumes API quota; the script pauses briefly between videos to be polite
- plotter.py pops up matplotlib windows, so run it where a display is available
- If the API returns no comments or quota is exceeded, some videos may produce no rows in the CSV

## Developers
-Karim El Assaad - 40127808
-Saad Khan - 40177298
-Mohamed-Rabah-Ishaq Loucif - 40282580
-Jean Naima - 40210371
-Maxence Roy - 40251806
-Veronique Touma - 40249766
-Jeremy Vieira - 40246737

