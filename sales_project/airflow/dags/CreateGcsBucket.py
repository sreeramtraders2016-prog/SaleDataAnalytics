from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="create_gcs_bucket_latest",
    start_date=datetime(2026, 5, 19),
    schedule=None,
    catchup=False
) as dag:

    create_bucket = BashOperator(
        task_id="create_gcs_bucket",
        bash_command="""
        export GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/keys/sodium-hope-496414-q7-67bd82e4d356.json

        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

        gcloud config set project sodium-hope-496414-q7

        if ! gcloud storage buckets describe gs://spalika-sales-data-2016 >/dev/null 2>&1; then
            gcloud storage buckets create gs://spalika_sales_data-2016 --location=US
        else
            echo "Bucket already exists" 
        fi
        """
    )

    create_bucket