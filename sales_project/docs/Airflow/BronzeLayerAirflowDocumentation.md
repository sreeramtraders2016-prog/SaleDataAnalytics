# Bronze Layer Airflow Documentation

## Project Overview

This project implements the Bronze Layer of a Medallion Architecture using:

- Apache Airflow
- Google BigQuery
- Google Cloud Storage (GCS)
- Google Cloud Platform (GCP)
- Docker & PostgreSQL

The Bronze Layer is responsible for ingesting raw source files from GCS into BigQuery raw tables without transformations.

---

# Architecture

```text
Source CSV Files
       ↓
Google Cloud Storage (GCS)
       ↓
Airflow DAG
       ↓
PythonOperator Tasks
       ↓
BigQuery Bronze Tables
```

---

# Objectives

The Bronze Layer pipeline performs:

- Raw data ingestion
- Schema-based loading
- Table creation in BigQuery
- Centralized orchestration with Airflow
- Logging and monitoring
- Parallel task execution

---

# Project Structure

```text
sales_project/
│
├── airflow/
│   ├── dags/
│   │   ├── BronzeSalesLoadDag.py
│   │   ├── CreateBigqueryDatasets.py
│   │   ├── CreateGcsBucket.py
│   │   └── UploadBronzeToGcs.py
│   │
│   ├── keys/
│   │   └── sodium-hope-496414-q7-67bd82e4d356.json
│   │
│   ├── logs/
│   ├── plugins/
│   └── docker-compose.yml
│
├── data/
├── schema/
├── sql/
├── spark_jobs/
├── notebooks/
└── dashboards/
```

---

# Docker Services

The Airflow environment is containerized using Docker Compose.

## Services Used

| Service | Purpose |
|---|---|
| postgres | Airflow metadata database |
| airflow-init | Initializes Airflow DB and admin user |
| airflow-webserver | Airflow UI |
| airflow-scheduler | Executes scheduled tasks |

---

# Docker Volume Mounts

```yaml
volumes:
  - ./dags:/opt/airflow/dags
  - ./keys:/opt/airflow/keys
  - ../schema:/opt/airflow/schema
  - ../data:/opt/airflow/data
```

These mounts allow Airflow containers to access:
- DAG files
- GCP credentials
- Schema JSON files
- Local datasets

---

# Authentication Setup

Authentication is performed using a GCP Service Account JSON key.

## Credential File

```text
airflow/keys/sodium-hope-496414-q7-67bd82e4d356.json
```

## Environment Variable

```yaml
GOOGLE_APPLICATION_CREDENTIALS:
/opt/airflow/keys/sodium-hope-496414-q7-67bd82e4d356.json
```

This enables Airflow tasks to authenticate with:
- BigQuery
- GCS

---

# Bronze Layer DAG

## DAG Name

```python
bronze_sales_load_dag
```

## DAG Responsibilities

The DAG:
1. Reads CSV files from GCS
2. Reads schema definitions from JSON files
3. Loads data into BigQuery Bronze tables

---

# Bronze Tables

| Source File | Bronze Table |
|---|---|
| cust_info.csv | crm_customers_raw |
| prd_info.csv | crm_products_raw |
| sales_details.csv | crm_sales_raw |
| ERP_CUST_AZ12.csv | erp_customer_extra_raw |
| ERP_LOC_A101.csv | erp_customer_loc_raw |
| ERP_PX_CAT_G1V2.csv | erp_product_category_raw |

Dataset:

```text
bronze_sales_ds
```

---

# DAG Task Design

Each table load is implemented as an independent `PythonOperator`.

## Benefits

- Parallel execution
- Independent retries
- Better observability
- Modular architecture
- Easier debugging

---

# PythonOperator Workflow

Each task:
1. Creates BigQuery client
2. Reads schema JSON
3. Configures BigQuery load job
4. Loads CSV from GCS
5. Writes into Bronze table

---

# Common Load Function

```python
def load_csv_to_bq(table_id, source_uri, schema_path):
```

This reusable function reduces code duplication across tasks.

---

# BigQuery Load Configuration

```python
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    write_disposition="WRITE_TRUNCATE",
)
```

---

# Schema Management

Schemas are maintained separately as JSON files.

Example:

```text
schema/crm_customers_schema.json
```

Advantages:
- Strong typing
- Data consistency
- Production-grade ingestion
- Easier schema evolution

---

# Airflow UI

Access Airflow UI:

```text
http://localhost:8080
```

Default Credentials:

```text
Username: admin
Password: admin
```

---

# Running the Environment

## Start Containers

```bash
docker compose up --build
```

## Stop Containers

```bash
docker compose down
```

---

# Monitoring

Airflow provides:
- DAG monitoring
- Task-level logs
- Retry management
- Scheduling visibility
- Execution history

---

# Logging

Task logs are available in:

```text
airflow/logs/
```

Logs include:
- authentication
- BigQuery load status
- task execution details
- failures and retries

---

# Error Handling

Common handled issues:
- missing credentials
- schema mismatches
- invalid CSV format
- missing GCS objects
- BigQuery permissions

---

# Advantages of This Design

## Scalability

Each table is modular and independently executable.

## Reusability

Single reusable load function.

## Production Readiness

- Dockerized
- Orchestrated
- Logged
- Retry-enabled
- Cloud-native

## Extensibility

Easy to extend to:
- Silver Layer
- Gold Layer
- Incremental loads
- SCD Type 2
- Data quality checks

---

# Future Enhancements

## Silver Layer

- Data cleaning
- Null handling
- Standardization
- Deduplication

## Gold Layer

- Star schema
- Fact tables
- Dimension tables
- KPI aggregations

## Additional Improvements

- Incremental loading
- Partitioned tables
- Airflow Variables
- Secret Manager integration
- Data validation framework
- SLA monitoring

---

# Conclusion

The Bronze Layer successfully establishes a scalable ingestion framework using Airflow and BigQuery. The implementation follows modern Data Engineering best practices with modular orchestration, reusable ingestion logic, and cloud-native architecture.

