FROM astronomerinc/ap-airflow:2.0.0

# Copy the DAGs from your repository into the Airflow container
COPY ./dags /usr/local/airflow/dags
