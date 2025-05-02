# fetch_trending_topics.py

from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from collections import Counter
import pandas as pd
import re
import html
import os

def fetch_trending_topics():
    api_key = os.getenv("AIzaSyBeuRk7payBeXDM-zbRtEoHXtXKUaOGQrM")  
    youtube = build('youtube', 'v3', developerKey=api_key)

    now = datetime.now(timezone.utc)
    two_hours_ago = now - timedelta(hours=2)
    published_after = two_hours_ago.isoformat("T")

    max_results_per_page = 50
    max_pages = 10
    all_videos = []
    next_page_token = None

    print(f"⏱️ Fetching videos published after: {published_after}\n")

    for _ in range(max_pages):
        request = youtube.search().list(
            part="snippet",
            maxResults=max_results_per_page,
            order="viewCount",
            publishedAfter=published_after,
            type="video",
            regionCode="US",
            pageToken=next_page_token
        )
        response = request.execute()
        items = response.get("items", [])
        all_videos.extend(items)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    print(f"✅ Total videos fetched: {len(all_videos)}\n")

    titles = [html.unescape(v['snippet']['title']) for v in all_videos]
    descriptions = [html.unescape(v['snippet'].get('description', '')) for v in all_videos]
    combined_text = " ".join(titles + descriptions)

    words = re.findall(r'\b\w+\b', combined_text.lower())

    stopwords = {
        "the", "is", "a", "an", "in", "of", "to", "and", "for", "this", "on", "with", "at",
        "it", "you", "from", "by", "that", "be", "as", "are", "i", "was", "we", "they", "your",
        "news", "live", "breaking", "update", "video", "watch", "official", "trailer",
        "www", "com", "http", "https", "channel", "new", "show", "episode", "shorts",
        "subscribe", "like", "join", "share", "comment", "youtube", "tv", "reels", "stream",
        "viral", "trending", "funny", "comedy", "explore", "amazing", "crazy", "ultimate",
        "best", "top", "wow", "insane", "emotional", "powerful", "must", "see", "epic", "unbelievable",
        "trailer", "review", "vlog", "reaction", "behind", "scenes", "challenge", "clip",
        "footage", "teaser", "premiere", "part", "full", "highlight", "recap",
        "official", "leaked", "meme", "skit", "today", "now", "latest", "daily", "weekly",
        "current", "before", "after", "soon", "how", "why", "what", "tips", "tricks", "tutorial",
        "guide", "step", "learn", "make", "do", "our", "مباشر", "الرياضي", "مباراة", "canlı",
        "en", "direct", "vivo", "dal", "прямой", "эфир", "लाइव", "লাইভ", "براہ", "راست",
        "langsung", "ライブ", "라이브", "直播", "yayÄ±n"
    }

    filtered_words = [word for word in words if word not in stopwords and len(word) > 2]
    keyword_counts = Counter(filtered_words)
    trending_keywords = keyword_counts.most_common(15)

    top_topics = [word for word, _ in trending_keywords[:5]]
    df = pd.DataFrame({"topic": top_topics})
    df.to_csv("/tmp/data/trending_topics.csv", index=False)

    print("📁 Top 5 trending topics saved to '/tmp/data/trending_topics.csv'")
    Add trending topics script
