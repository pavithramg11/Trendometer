# Trendometer

Trendometer is a data pipeline project that analyzes trending topics and sentiment on YouTube using Apache Airflow, Python, and Docker. It automates the fetching, sentiment analysis, and visualization of trending content to provide insight into online discussions and mood over time.

 Features
	•	Automated Data Pipeline using Apache Airflow
	•	Trending Topic Fetching from YouTube
	•	Sentiment Analysis using NLP techniques
	•	Graph Generation for trend visualization
	•	Containerized with Docker for easy deployment

 Trendometer/
│
├── dags/
│   └── youtube_sentiment_dag.py      # Airflow DAG for orchestrating the pipeline
│
├── scripts/
│   ├── fetch_trending_topics.py      # Retrieves trending YouTube topics
│   ├── analyze_sentiment.py          # Performs sentiment analysis on content
│   └── generate_graphs.py            # Generates sentiment trend graphs
│
├── Dockerfile                        # Container configuration for deployment
├── requirements.txt                  # Python dependencies

Getting Started
Prerequisites
	•	Docker
	•	Python 3.8+
	•	(Optional) Apache Airflow locally or via Docker Compose

 Installation
	1.	Clone the repository:
     git clone https://github.com/yourusername/trendometer.git
     cd trendometer-main
	2.	Build the Docker image:
 docker build -t trendometer .
 	3.	Run your container (Airflow config recommended):
  docker run -p 8080:8080 trendometer


  Running the DAG
	1.	Start Airflow web UI (default: http://localhost:8080)
	2.	Enable and trigger the DAG: youtube_sentiment_dag
	3.	Monitor tasks and view outputs


 Output
	•	Sentiment-labeled trending topics
	•	Time-series visualizations of trending sentiment
	•	Exportable reports or plots (saved by generate_graphs.py)

 Technologies Used
	•	Python
	•	Apache Airflow
	•	Docker
	•	NLP / Sentiment Analysis
	•	Matplotlib / Plotly (for graphs)
	•	YouTube API (or custom scraping, depending on script config)

