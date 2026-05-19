from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from google.cloud import bigquery

# =====================================================
# BIGQUERY CLIENT
# =====================================================


# =====================================================
# COMMON LOAD FUNCTION
# =====================================================

def load_csv_to_bq(table_id, source_uri, schema_path):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema=[],
    )

    # Load schema from JSON file
    import json

    with open(schema_path, "r") as f:
        schema_json = json.load(f)

    job_config.schema = [
        bigquery.SchemaField(
            field["name"],
            field["type"],
            mode=field.get("mode", "NULLABLE")
        )
        for field in schema_json
    ]

    load_job = client.load_table_from_uri(
        source_uri,
        table_id,
        job_config=job_config
    )

    load_job.result()

    print(f"Loaded data into {table_id}")


# =====================================================
# DAG
# =====================================================

with DAG(
    dag_id="bronze_sales_load_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["bronze"],
) as dag:

    # =================================================
    # CRM CUSTOMERS
    # =================================================

    load_crm_customers = PythonOperator(
        task_id="load_crm_customers",
        python_callable=load_csv_to_bq,
        op_kwargs={
            "table_id": "bronze_sales_ds.crm_customers_raw",
            "source_uri": "gs://spalika_sales_data-2016/raw/cust_info.csv",
            "schema_path": "/opt/airflow/schema/crm_customers_schema.json",
        },
    )

    # =================================================
    # CRM PRODUCTS
    # =================================================

    load_crm_products = PythonOperator(
        task_id="load_crm_products",
        python_callable=load_csv_to_bq,
        op_kwargs={
            "table_id": "bronze_sales_ds.crm_products_raw",
            "source_uri": "gs://spalika_sales_data-2016/raw/prd_info.csv",
            "schema_path": "/opt/airflow/schema/crm_products_schema.json",
        },
    )

    # =================================================
    # CRM SALES
    # =================================================

    load_crm_sales = PythonOperator(
        task_id="load_crm_sales",
        python_callable=load_csv_to_bq,
        op_kwargs={
            "table_id": "bronze_sales_ds.crm_sales_raw",
            "source_uri": "gs://spalika_sales_data-2016/raw/sales_details.csv",
            "schema_path": "/opt/airflow/schema/crm_sales_schema.json",
        },
    )

    # =================================================
    # ERP CUSTOMER EXTRA
    # =================================================

    load_erp_customer_extra = PythonOperator(
        task_id="load_erp_customer_extra",
        python_callable=load_csv_to_bq,
        op_kwargs={
            "table_id": "bronze_sales_ds.erp_customer_extra_raw",
            "source_uri": "gs://spalika_sales_data-2016/raw/ERP_CUST_AZ12.csv",
            "schema_path": "/opt/airflow/schema/erp_customer_extra_schema.json",
        },
    )

    # =================================================
    # ERP CUSTOMER LOCATION
    # =================================================

    load_erp_customer_loc = PythonOperator(
        task_id="load_erp_customer_loc",
        python_callable=load_csv_to_bq,
        op_kwargs={
            "table_id": "bronze_sales_ds.erp_customer_loc_raw",
            "source_uri": "gs://spalika_sales_data-2016/raw/ERP_LOC_A101.csv",
            "schema_path": "/opt/airflow/schema/erp_customer_loc_schema.json",
        },
    )

    # =================================================
    # ERP PRODUCT CATEGORY
    # =================================================

    load_erp_product_category = PythonOperator(
        task_id="load_erp_product_category",
        python_callable=load_csv_to_bq,
        op_kwargs={
            "table_id": "bronze_sales_ds.erp_product_category_raw",
            "source_uri": "gs://spalika_sales_data-2016/raw/ERP_PX_CAT_G1V2.csv",
            "schema_path": "/opt/airflow/schema/erp_product_category_schema.json",
        },
    )

    # =================================================
    # TASK FLOW
    # =================================================

    [
        load_crm_customers,
        load_crm_products,
        load_crm_sales,
        load_erp_customer_extra,
        load_erp_customer_loc,
        load_erp_product_category,
    ]