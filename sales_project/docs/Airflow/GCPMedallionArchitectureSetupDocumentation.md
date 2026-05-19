# GCP Medallion Architecture Setup Documentation

# Project Overview

This document describes the setup and implementation of:

* Google Cloud Storage (GCS) Bucket Creation
* Uploading Local Files to GCS
* BigQuery Dataset Creation for Medallion Architecture
* Apache Airflow Orchestration

The project follows a Medallion Architecture consisting of:

* Bronze Layer
* Silver Layer
* Gold Layer

Technologies used:

* Apache Airflow
* Google Cloud Platform (GCP)
* Google Cloud Storage (GCS)
* Google BigQuery
* Docker
* PostgreSQL
* Python

---

# Medallion Architecture Overview

```text
Local CSV Files
        ↓
Google Cloud Storage (GCS)
        ↓
Bronze Layer (Raw Data)
        ↓
Silver Layer (Cleaned Data)
        ↓
Gold Layer (Business Analytics)
```

---

# Project Structure

```text
sales_project/
│
├── airflow/
│   ├── dags/
│   │   ├── CreateGcsBucket.py
│   │   ├── UploadBronzeToGcs.py
│   │   ├── CreateBigqueryDatasets.py
│   │   └── BronzeSalesLoadDag.py
│   │
│   ├── keys/
│   ├── logs/
│   ├── plugins/
│   └── docker-compose.yml
│
├── data/
├── schema/
├── sql/
├── notebooks/
├── spark_jobs/
└── dashboards/
```

---

# Google Cloud Storage (GCS) Bucket Creation

## Objective

Create a centralized cloud storage bucket for storing raw datasets.

---

# Bucket Details

| Property     | Value                  |
| ------------ | ---------------------- |
| Bucket Name  | spalika_sales_data     |
| Storage Type | Standard               |
| Location     | US                     |
| Purpose      | Store source CSV files |

---

# Airflow DAG: CreateGcsBucket.py

## Purpose

Creates a GCS bucket programmatically using Python.

---

# Python Libraries Used

```python
from google.cloud import storage
```

---

# Workflow

```text
Airflow DAG
      ↓
PythonOperator
      ↓
Google Cloud Storage Client
      ↓
Create GCS Bucket
```

---

# Sample Logic

```python
from google.cloud import storage

client = storage.Client()

bucket = client.bucket("spalika_sales_data")
bucket.location = "US"

client.create_bucket(bucket)
```

---

# Benefits

* Automated bucket provisioning
* Cloud-native storage
* Centralized raw data storage
* Reusable pipeline setup

---

# Upload Local Files to GCS

## Objective

Upload raw CSV files from local storage into the GCS bucket.

---

# Source Files

| Local File          | GCS Destination                                  |
| ------------------- | ------------------------------------------------ |
| cust_info.csv       | gs://spalika_sales_data/data/cust_info.csv       |
| prd_info.csv        | gs://spalika_sales_data/data/prd_info.csv        |
| sales_details.csv   | gs://spalika_sales_data/data/sales_details.csv   |
| ERP_CUST_AZ12.csv   | gs://spalika_sales_data/data/ERP_CUST_AZ12.csv   |
| ERP_LOC_A101.csv    | gs://spalika_sales_data/data/ERP_LOC_A101.csv    |
| ERP_PX_CAT_G1V2.csv | gs://spalika_sales_data/data/ERP_PX_CAT_G1V2.csv |

---

# Airflow DAG: UploadBronzeToGcs.py

## Purpose

Uploads local CSV files into the GCS bucket.

---

# Workflow

```text
Local Files
      ↓
PythonOperator
      ↓
GCS Client
      ↓
Upload Files to Bucket
```

---

# Python Libraries Used

```python
from google.cloud import storage
```

---

# Sample Upload Logic

```python
from google.cloud import storage

client = storage.Client()

bucket = client.bucket("spalika_sales_data")

blob = bucket.blob("data/cust_info.csv")
blob.upload_from_filename("/opt/airflow/data/cust_info.csv")
```

---

# Benefits

* Automated cloud ingestion
* Centralized storage layer
* Easy integration with BigQuery
* Airflow orchestration support

---

# BigQuery Dataset Creation

## Objective

Create datasets representing Medallion Architecture layers.

---

# Medallion Datasets

| Layer  | Dataset Name    | Purpose                        |
| ------ | --------------- | ------------------------------ |
| Bronze | bronze_sales_ds | Raw ingestion tables           |
| Silver | silver_sales_ds | Cleaned and transformed data   |
| Gold   | gold_sales_ds   | Analytics and reporting tables |

---

# Airflow DAG: CreateBigqueryDatasets.py

## Purpose

Creates BigQuery datasets for Bronze, Silver, and Gold layers.

---

# Workflow

```text
Airflow DAG
      ↓
PythonOperator
      ↓
BigQuery Client
      ↓
Create Datasets
```

---

# Python Libraries Used

```python
from google.cloud import bigquery
```

---

# Sample Dataset Creation Logic

```python
from google.cloud import bigquery

client = bigquery.Client()

bronze_dataset = bigquery.Dataset("project_id.bronze_sales_ds")
bronze_dataset.location = "US"

client.create_dataset(bronze_dataset, exists_ok=True)
```

---

# Benefits

* Layered architecture
* Better data organization
* Easier governance
* Scalable analytics pipeline

---

# Airflow Orchestration

## Purpose

Airflow orchestrates:

1. Bucket creation
2. File uploads
3. Dataset creation
4. Bronze table loading

---

# Airflow Services

| Service           | Purpose             |
| ----------------- | ------------------- |
| airflow-webserver | UI and monitoring   |
| airflow-scheduler | Executes tasks      |
| airflow-init      | Initializes Airflow |
| postgres          | Metadata database   |

---

# Docker Compose Setup

## Volume Mounts

```yaml
volumes:
  - ./dags:/opt/airflow/dags
  - ./keys:/opt/airflow/keys
  - ../data:/opt/airflow/data
  - ../schema:/opt/airflow/schema
```

---

# Authentication Setup

## Service Account Key

```text
airflow/keys/sodium-hope-496414-q7-67bd82e4d356.json
```

---

# Environment Variable

```yaml
GOOGLE_APPLICATION_CREDENTIALS:
/opt/airflow/keys/sodium-hope-496414-q7-67bd82e4d356.json
```

---

# Airflow UI

## URL

```text
http://localhost:8080
```

## Default Credentials

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

---

## Stop Containers

```bash
docker compose down
```

---

# Monitoring and Logs

Airflow provides:

* DAG monitoring
* Task-level execution logs
* Retry management
* Scheduling visibility
* Dependency tracking

---

# Advantages of This Architecture

## Scalability

Supports future expansion for:

* Spark processing
* Incremental loading
* Streaming pipelines
* Data warehousing

---

## Cloud-Native Design

* GCS for storage
* BigQuery for analytics
* Airflow for orchestration
* Dockerized deployment

---

## Production Readiness

* Modular workflows
* Retry mechanisms
* Logging and monitoring
* Independent task execution

---

# Future Enhancements

## Bronze Layer

* Incremental ingestion
* Partitioned tables
* File validation

---

## Silver Layer

* Data cleansing
* Standardization
* Deduplication
* Data quality checks

---

## Gold Layer

* Fact tables
* Dimension tables
* KPI aggregations
* BI dashboards

---

# Conclusion

This implementation establishes a complete cloud-native Medallion Architecture foundation using Airflow, GCS, and BigQuery. The system automates infrastructure provisioning, file ingestion, dataset creation, and raw data loading while maintaining scalability and production readiness.
