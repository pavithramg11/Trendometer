from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from scripts.fetch_trending_topics import fetch_trending_topics
from scripts.analyze_sentiment import analyze_sentiment
from scripts.generate_graphs import generate_graphs

default_args = {
    'owner': 'ANP',
    'start_date': datetime(2024, 4, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'youtube_sentiment_dag',
    default_args=default_args,
    schedule_interval='0 */3 * * *',  # Every 3 hours
    catchup=False
)

task1 = PythonOperator(
    task_id='fetch_trending',
    python_callable=fetch_trending_topics,
    dag=dag
)

task2 = PythonOperator(
    task_id='analyze_sentiment',
    python_callable=analyze_sentiment,
    dag=dag
)

task3 = PythonOperator(
    task_id='generate_graphs',
    python_callable=generate_graphs,
    dag=dag
)

task1 >> task2 >> task3
