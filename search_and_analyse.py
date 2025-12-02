import time

import pandas as pd
from googleapiclient.discovery import build

from anaylze_spam_model import analyze_video_for_links

YOUTUBE_API_KEY = "api"
RESULTS_CSV = "video_link_results.csv"
VIDEOS_PER_SUBJECT = 10

SUBJECTS = [
    "Canadian politics",
    "Canadian news",
    "Canadian entertainment",
    "Canadian sports",
    "Canadian technology",
    "Canadian economy",
    "Canadian culture",
    "Canadian history",
    "Canadian education",
    "Canadian healthcare",
    "Canadian travel & tourism",
    "Canadian environment & climate",
    "Canadian Indigenous issues",
    "Canadian science",
    "Canadian business",
    "Canadian weather events",
    "Canadian crime & justice",
    "Canadian military",
    "Canadian government updates",
    "Canadian social issues",
    "Canadian music",
    "Canadian movies & TV shows",
    "Canadian food",
    "Canadian festivals & events"
]

def youtube_search(query, max_results=5):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY, cache_discovery=False)
    request = youtube.search().list(
        q=query, part="id", type="video", maxResults=max_results,
        order="relevance", regionCode="CA"
    )
    response = request.execute()
    return [f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in response.get("items", [])]

def main():
    final_results = []

    for subject in SUBJECTS:
        print(f"\n[INFO] Searching for: {subject}")
        videos = youtube_search(subject, VIDEOS_PER_SUBJECT)
        for url in videos:
            print(f"[INFO] Analyzing: {url}")
            results = analyze_video_for_links(url)
            for r in results:
                r["subject"] = subject
                r["video_url"] = url
                final_results.append(r)
            time.sleep(1)

    if final_results:
        pd.DataFrame(final_results).to_csv(RESULTS_CSV, index=False)
        print(f"Saved results to {RESULTS_CSV}")
    else:
        print("No results to save.")

if __name__ == "__main__":
    main()
