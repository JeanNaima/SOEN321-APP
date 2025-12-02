import re
import warnings
from urllib.parse import urlparse, parse_qs

import pandas as pd
from joblib import load
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_KEY = "api"
DEFAULT_MAX_COMMENTS = 300

LINK_PATTERN = re.compile(
    r"""
    \b(                       
        https?://[^\s]+       
        | www\.[^\s]+         
        | (?:[a-z0-9-]+\.)+   
          (?:com|net|org|co|io|ca|uk|de|app|xyz|info|biz|gov|edu|news|be|ch|it) 
          \b               
          (?:/[^\s]*)?        
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

DOMAIN_PATTERN = re.compile(
    r"\b(?:https?://|www\.)?((?:[a-z0-9-]+\.)+(?:com|net|org|co|io|ca|uk|de|app|xyz|info|biz|gov|edu|news|be|ch|it))\b",
    re.IGNORECASE,
)


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        if parsed.path == "/watch":
            query = parse_qs(parsed.query)
            return query.get("v", [""])[0]
        parts = parsed.path.strip("/").split("/")
        if parts and parts[0] in ("shorts", "embed"):
            return parts[1] if len(parts) > 1 else ""
    if parsed.hostname == "youtu.be":
        return parsed.path.strip("/")
    return ""


def fetch_comments(video_id: str, max_comments: int = DEFAULT_MAX_COMMENTS):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    comments = []
    next_page_token = None
    try:
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText",
                order="time",
            )
            response = request.execute()
            for item in response.get("items", []):
                text = item["snippet"]["topLevelComment"]["snippet"].get("textDisplay", "")
                comments.append(text)
                if len(comments) >= max_comments:
                    break
            if len(comments) >= max_comments:
                break
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
    except HttpError as e:
        warnings.warn(f"Could not fetch comments for video {video_id}: {e}")
        return []
    return comments


def comment_has_link(text: str) -> bool:
    """Return True if the comment text looks like it contains a URL/domain."""
    if not isinstance(text, str):
        return False
    return bool(LINK_PATTERN.search(text))


def extract_first_domain(text: str) -> str:
    """Extract the first domain-like token from text."""
    if not isinstance(text, str):
        return ""
    match = DOMAIN_PATTERN.search(text.lower())
    if not match:
        return ""
    return match.group(1)


def categorize_domain(domain: str) -> str:
    """Assign a coarse category to a domain string."""
    if not domain:
        return "no_link"
    if any(k in domain for k in ("youtube.com", "youtu.be")):
        return "video_platform"
    if "wikipedia.org" in domain:
        return "wikipedia"
    if any(k in domain for k in ("facebook.com", "fb.com", "instagram.com", "tiktok.com", "twitter.com", "x.com", "reddit.com")):
        return "social"
    if any(k in domain for k in ("bit.ly", "tinyurl", "goo.gl", "t.co", "ow.ly", "is.gd")):
        return "link_shortener"
    if any(k in domain for k in ("amazon.", "ebay.", "shopify", "etsy.", "aliexpress", "mercado")):
        return "ecommerce"
    if any(k in domain for k in ("binance", "coinbase", "kraken", "crypto", "btc", "ethereum", "eth", "defi", "nft")):
        return "crypto"
    if any(k in domain for k in ("drive.google.com", "dropbox", "mega.nz", "wetransfer")):
        return "file_share"
    if any(k in domain for k in ("whatsapp.com", "wa.me", "telegram", "discord", "signal.org")):
        return "messaging"
    return "generic_link"


def simple_clean(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

def analyze_video_for_links(url: str, max_comments: int = DEFAULT_MAX_COMMENTS):
    """Return list of comment dicts with HAS_LINK flag for a video URL."""
    video_id = extract_video_id(url)
    if not video_id:
        print(f"[ERROR] Could not extract video ID from URL: {url}")
        return []

    comments = fetch_comments(video_id, max_comments=max_comments)
    if not comments:
        return []

    results = []
    for text in comments:
        has_link = comment_has_link(text)
        domain = extract_first_domain(text) if has_link else ""
        results.append(
            {
                "CONTENT": text,
                "HAS_LINK": has_link,
                "LINK_DOMAIN": domain,
                "LINK_CATEGORY": categorize_domain(domain),
            }
        )
    return results
