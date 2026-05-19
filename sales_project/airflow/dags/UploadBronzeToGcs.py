from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================

PROJECT_ID = "sodium-hope-496414-q7"

BUCKET_NAME = "spalika_sales_data-2016"

LOCAL_DATA_PATH = "/opt/airflow/data/bronze"

SERVICE_ACCOUNT_KEY = "/opt/airflow/keys/sodium-hope-496414-q7-67bd82e4d356.json"

# =====================================================
# DAG
# =====================================================

with DAG(
    dag_id="upload_bronze_to_gcs",
    start_date=datetime(2026, 5, 19),
    schedule=None,
    catchup=False,
    tags=["gcs", "bronze", "sales_project"]
) as dag:

    upload_files_to_gcs = BashOperator(
        task_id="upload_files_to_gcs",

        bash_command=f"""
        export GOOGLE_APPLICATION_CREDENTIALS={SERVICE_ACCOUNT_KEY}

        gcloud auth activate-service-account \
            --key-file=$GOOGLE_APPLICATION_CREDENTIALS

        gcloud config set project {PROJECT_ID}

        echo "Uploading Bronze CSV files to GCS..."

        gsutil cp {LOCAL_DATA_PATH}/*.csv \
        gs://{BUCKET_NAME}/raw/

        echo "Upload Completed"
        """
    )

    upload_files_to_gcs