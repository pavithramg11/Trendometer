# analyze_sentiment.py

import torch
from transformers import pipeline
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from collections import Counter
import pandas as pd
import os

def analyze_sentiment():
    # Load API key from environment variable
    api_key = os.getenv("AIzaSyBeuRk7payBeXDM-zbRtEoHXtXKUaOGQrM")
    youtube = build('youtube', 'v3', developerKey=api_key)

    classifier = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment",
        tokenizer="cardiffnlp/twitter-roberta-base-sentiment",
        device=0 if torch.cuda.is_available() else -1
    )

    label_map = {
        "LABEL_0": "NEGATIVE",
        "LABEL_1": "NEUTRAL",
        "LABEL_2": "POSITIVE"
    }

    def fetch_video_texts(topic, max_results=5):
        now = datetime.now(timezone.utc)
        two_days_ago = now - timedelta(days=2)
        published_after = two_days_ago.isoformat("T")

        search_response = youtube.search().list(
            part="snippet",
            q=topic,
            maxResults=max_results,
            order="relevance",
            type="video",
            publishedAfter=published_after
        ).execute()

        texts = []
        video_ids = []

        for item in search_response.get("items", []):
            title = item["snippet"]["title"]
            desc = item["snippet"].get("description", "")
            combined = f"{title} {desc}"
            texts.append(combined)
            video_ids.append(item["id"]["videoId"])

        return texts, video_ids

    def get_comments(video_id, max_comments=50):
        comments = []
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)
                if len(comments) >= max_comments:
                    break
        except Exception as e:
            print(f"❌ Error fetching comments for {video_id}: {e}")
        return comments

    def run_analysis(texts):
        cleaned = [t[:500] for t in texts if len(t.strip()) > 0]
        results = classifier(cleaned, batch_size=8)
        return Counter([label_map[r["label"]] for r in results]), results

    def analyze_topic_sentiment(topic):
        print(f"\n🔍 Analyzing topic: {topic}")
        title_texts, video_ids = fetch_video_texts(topic)
        title_sentiment, _ = run_analysis(title_texts)

        all_comments = []
        for vid in video_ids:
            all_comments.extend(get_comments(vid))
        comment_sentiment, comment_results = run_analysis(all_comments)

        all_texts = title_texts + all_comments
        _, all_results = run_analysis(all_texts)
        sentiment_texts = {"POSITIVE": [], "NEGATIVE": [], "NEUTRAL": []}
        for i, res in enumerate(all_results):
            sentiment = label_map[res["label"]]
            sentiment_texts[sentiment].append(all_texts[i])

        def score(counter):
            total = sum(counter.values())
            return {
                "NEGATIVE": counter["NEGATIVE"] / total if total else 0,
                "NEUTRAL":  counter["NEUTRAL"]  / total if total else 0,
                "POSITIVE": counter["POSITIVE"] / total if total else 0
            }

        title_score = score(title_sentiment)
        comment_score = score(comment_sentiment)

        final_score = {
            s: round(0.3 * title_score.get(s, 0) + 0.7 * comment_score.get(s, 0), 3)
            for s in ["NEGATIVE", "NEUTRAL", "POSITIVE"]
        }

        print(f"🎥 Title Sentiment: {dict(title_sentiment)}")
        print(f"💬 Comment Sentiment: {dict(comment_sentiment)}")
        print(f"📊 Final Sentiment for '{topic}': {final_score}")

        return {
            **final_score,
            "topic": topic,
            "all_text": " ".join(all_texts),
            "positive_text": " ".join(sentiment_texts["POSITIVE"]),
            "negative_text": " ".join(sentiment_texts["NEGATIVE"]),
            "neutral_text": " ".join(sentiment_texts["NEUTRAL"])
        }

    # ------------------ Main Run ------------------

    input_csv = "/tmp/data/trending_topics.csv"
    df_topics = pd.read_csv(input_csv)
    topics = df_topics["topic"].tolist()

    sentiment_data = []
    wordcloud_texts = []

    for topic in topics:
        result = analyze_topic_sentiment(topic)
        sentiment_data.append({k: result[k] for k in ["topic", "NEGATIVE", "NEUTRAL", "POSITIVE"]})
        wordcloud_texts.append({
            "topic": result["topic"],
            "all_text": result["all_text"],
            "positive_text": result["positive_text"],
            "negative_text": result["negative_text"],
            "neutral_text": result["neutral_text"]
        })

    os.makedirs("/tmp/data", exist_ok=True)
    pd.DataFrame(sentiment_data).to_csv("/tmp/data/sentiment_scores.csv", index=False)
    pd.DataFrame(wordcloud_texts).to_csv("/tmp/data/wordcloud_texts.csv", index=False)

    print("✅ Sentiment and word cloud data saved to /tmp/data/")
    Add sentiment analysis script
