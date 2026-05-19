from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================

PROJECT_ID = "sodium-hope-496414-q7"

SERVICE_ACCOUNT_KEY = "/opt/airflow/keys/sodium-hope-496414-q7-67bd82e4d356.json"

# =====================================================
# DAG
# =====================================================

with DAG(
    dag_id="create_bigquery_datasets",
    start_date=datetime(2026, 5, 19),
    schedule=None,
    catchup=False,
    tags=["bigquery", "setup", "sales_project"]
) as dag:

    create_datasets = BashOperator(
        task_id="create_datasets",

        bash_command=f"""
        export GOOGLE_APPLICATION_CREDENTIALS={SERVICE_ACCOUNT_KEY}

        gcloud auth activate-service-account \
        --key-file=$GOOGLE_APPLICATION_CREDENTIALS

        gcloud config set project {PROJECT_ID}

        echo "Creating Bronze Dataset..."

        bq --location=US mk --dataset --description "Bronze Layer Dataset" \
        {PROJECT_ID}:bronze_sales_ds || echo "bronze_sales_ds already exists"

        echo "Creating Silver Dataset..."

        bq --location=US mk --dataset --description "Silver Layer Dataset" \
        {PROJECT_ID}:silver_sales_ds || echo "silver_sales_ds already exists"

        echo "Creating Gold Dataset..."

        bq --location=US mk --dataset --description "Gold Layer Dataset" \
        {PROJECT_ID}:gold_sales_ds || echo "gold_sales_ds already exists"

        echo "All datasets created successfully"
        """
    )

    create_datasets