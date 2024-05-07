from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import json
import os


def fetch_cnb_data():
    # URL for the CNB daily exchange rate API
    url = "https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.txt"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the data to a file in the Airflow file system
        data_path = os.path.join(os.getenv('AIRFLOW_HOME'), 'data')
        os.makedirs(data_path, exist_ok=True)
        file_path = os.path.join(data_path, f"cnb_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
        with open(file_path, 'w') as file:
            file.write(response.text)
    else:
        raise Exception("Failed to fetch data from CNB API")


# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['your-email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'cnb_data_dag',
    default_args=default_args,
    description='DAG for fetching CNB data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define the task
fetch_data_task = PythonOperator(
    task_id='fetch_cnb_data',
    python_callable=fetch_cnb_data,
    dag=dag,
)