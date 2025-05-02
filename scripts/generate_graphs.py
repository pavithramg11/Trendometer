# generate_graphs.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

def generate_graphs():
    print("📊 Generating visualizations...")

    # Load sentiment scores
    scores_path = "/tmp/data/sentiment_scores.csv"
    wordcloud_path = "/tmp/data/wordcloud_texts.csv"
    df_scores = pd.read_csv(scores_path)
    df_wc = pd.read_csv(wordcloud_path)

    # --- Grouped Bar Chart ---
    sns.set(style="whitegrid")
    df_melted = df_scores.melt(id_vars="topic", var_name="Sentiment", value_name="Score")

    plt.figure(figsize=(12, 6))
    sns.barplot(x="topic", y="Score", hue="Sentiment", data=df_melted)
    plt.xticks(rotation=45, ha='right')
    plt.title("Sentiment Distribution per Topic")
    plt.tight_layout()

    os.makedirs("/tmp/data", exist_ok=True)
    bar_chart_path = "/tmp/data/sentiment_bar_plot.png"
    plt.savefig(bar_chart_path)
    print(f"✅ Sentiment bar chart saved to: {bar_chart_path}")
    plt.close()

    # --- Word Cloud from POSITIVE text ---
    text = " ".join(df_wc["positive_text"].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("WordCloud - Positive Sentiment")

    wordcloud_path = "/tmp/data/wordcloud_positive.png"
    plt.savefig(wordcloud_path)
    print(f"✅ WordCloud saved to: {wordcloud_path}")
    plt.close()

    print("✅ Visualization generation complete.")
    Add graph generation script
