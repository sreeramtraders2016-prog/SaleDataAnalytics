# Sales Analytics Project – Bronze Layer Ingestion Documentation

# Project Overview

This document describes the Bronze Layer ingestion process implemented for the Sales Analytics Project using:

- Google Cloud Storage (GCS)
- Google BigQuery
- JSON Schema-based ingestion
- Medallion Architecture

The project follows the Bronze → Silver → Gold architecture pattern.

---

# Architecture Overview

```text
Source CSV Files
        ↓
Google Cloud Storage (Landing Zone)
        ↓
Bronze Layer (Raw BigQuery Tables)
        ↓
Silver Layer (Cleaned & Validated Tables)
        ↓
Gold Layer (Fact & Dimension Tables)
```

---

# Technology Stack

| Component | Technology |
|---|---|
| Cloud Storage | Google Cloud Storage |
| Data Warehouse | BigQuery |
| Data Source | CSV Files |
| Schema Management | JSON Schema |
| Query Engine | BigQuery SQL |
| Command Line Tools | gcloud, bq |

---

# Google Cloud Storage Setup

## Create Storage Bucket

```bash
gcloud storage buckets create gs://spalika_sales_data
```

---

## Verify Bucket

```bash
gcloud storage ls
```

---

# Upload Source Files to GCS

## Upload CSV Files

```bash
gcloud storage cp "C:\Sreenivas\sales\sales_project\data\*.csv" gs://spalika_sales_data/data/
```

---

## Verify Uploaded Files

```bash
gcloud storage ls gs://spalika_sales_data/data/
```

Uploaded files:

- cust_info.csv
- prd_info.csv
- sales_details.csv
- ERP_CUST_AZ12.csv
- ERP_LOC_A101.csv
- ERP_PX_CAT_G1V2.csv

---

# Dataset Creation

## Create Bronze Dataset

```bash
bq mk -d bronze_sales_ds
```

## Create Silver Dataset

```bash
bq mk -d silver_sales_ds
```

## Create Gold Dataset

```bash
bq mk -d gold_sales_ds
```

---

# Bronze Layer Design Principles

The Bronze layer stores raw source data exactly as received.

## Bronze Layer Rules

- All columns stored as STRING
- No transformations
- Preserve source format
- Support schema evolution
- Maintain auditability

---

# Schema Storage Structure

```text
sales_project/
│
├── data/
├── schema/
├── sql/
├── docs/
└── notebooks/
```

---

# Bronze Layer Tables

| Source File | Bronze Table |
|---|---|
| cust_info.csv | bronze_sales_ds.crm_customers_raw |
| prd_info.csv | bronze_sales_ds.crm_products_raw |
| sales_details.csv | bronze_sales_ds.crm_sales_raw |
| ERP_CUST_AZ12.csv | bronze_sales_ds.erp_customer_extra_raw |
| ERP_LOC_A101.csv | bronze_sales_ds.erp_customer_loc_raw |
| ERP_PX_CAT_G1V2.csv | bronze_sales_ds.erp_product_category_raw |

---

# Schema Files

| Schema File | Purpose |
|---|---|
| crm_customers_schema.json | Customer raw schema |
| crm_products_schema.json | Product raw schema |
| crm_sales_schema.json | Sales raw schema |
| erp_customer_extra_schema.json | ERP customer extra schema |
| erp_customer_loc_schema.json | ERP customer location schema |
| erp_product_category_schema.json | ERP product category schema |

---

# BigQuery Load Commands

## Load CRM Customers

```bash
bq load --source_format=CSV --skip_leading_rows=1 bronze_sales_ds.crm_customers_raw gs://spalika_sales_data/data/cust_info.csv "C:\Sreenivas\sales\sales_project\schema\crm_customers_schema.json"
```

## Verify Data

```bash
bq head bronze_sales_ds.crm_customers_raw
```

---

## Load CRM Products

```bash
bq load --source_format=CSV --skip_leading_rows=1 bronze_sales_ds.crm_products_raw gs://spalika_sales_data/data/prd_info.csv "C:\Sreenivas\sales\sales_project\schema\crm_products_schema.json"
```

## Verify Data

```bash
bq head bronze_sales_ds.crm_products_raw
```

---

## Load CRM Sales

```bash
bq load --source_format=CSV --skip_leading_rows=1 bronze_sales_ds.crm_sales_raw gs://spalika_sales_data/data/sales_details.csv "C:\Sreenivas\sales\sales_project\schema\crm_sales_schema.json"
```

## Verify Data

```bash
bq head bronze_sales_ds.crm_sales_raw
```

---

## Load ERP Customer Extra

```bash
bq load --source_format=CSV --skip_leading_rows=1 bronze_sales_ds.erp_customer_extra_raw gs://spalika_sales_data/data/ERP_CUST_AZ12.csv "C:\Sreenivas\sales\sales_project\schema\erp_customer_extra_schema.json"
```

## Verify Data

```bash
bq head bronze_sales_ds.erp_customer_extra_raw
```

---

## Load ERP Customer Location

```bash
bq load --source_format=CSV --skip_leading_rows=1 bronze_sales_ds.erp_customer_loc_raw gs://spalika_sales_data/data/ERP_LOC_A101.csv "C:\Sreenivas\sales\sales_project\schema\erp_customer_loc_schema.json"
```

## Verify Data

```bash
bq head bronze_sales_ds.erp_customer_loc_raw
```

---

## Load ERP Product Category

```bash
bq load --source_format=CSV --skip_leading_rows=1 bronze_sales_ds.erp_product_category_raw gs://spalika_sales_data/data/ERP_PX_CAT_G1V2.csv "C:\Sreenivas\sales\sales_project\schema\erp_product_category_schema.json"
```

## Verify Data

```bash
bq head bronze_sales_ds.erp_product_category_raw
```

---

# Data Validation Strategy

## Bronze Layer

Validation performed:

- File existence check
- CSV format validation
- Header validation
- Schema application

No business transformations are applied in Bronze.

---

# Silver Layer Responsibilities

The Silver layer will perform:

- Data type casting
- Null handling
- Duplicate removal
- Standardization
- Schema validation
- Data quality checks

Example:

- STRING → INT64
- STRING → DATE
- Missing values handling

---

# Gold Layer Responsibilities

The Gold layer will contain:

## Dimension Tables

- dim_customer
- dim_product
- dim_date
- dim_location

## Fact Tables

- fact_sales

---

# Naming Conventions

## Datasets

| Layer | Dataset |
|---|---|
| Bronze | bronze_sales_ds |
| Silver | silver_sales_ds |
| Gold | gold_sales_ds |

---

## Table Naming

| Pattern | Example |
|---|---|
| Raw tables | crm_customers_raw |
| Cleaned tables | crm_customers |
| Dimension tables | dim_customer |
| Fact tables | fact_sales |

---

# Best Practices Followed

- Medallion architecture implementation
- Separation of raw and curated layers
- Schema-driven ingestion
- Cloud Storage landing zone
- BigQuery centralized warehouse
- Reusable JSON schemas
- Modular ingestion process

---

# Future Enhancements

Planned improvements:

- Incremental loading
- Partitioned BigQuery tables
- Clustering optimization
- Airflow orchestration
- Data quality framework
- Automated schema validation
- CI/CD deployment

---

# Conclusion

The Bronze layer ingestion pipeline successfully:

- Stores raw source files in GCS
- Loads data into BigQuery Bronze tables
- Uses reusable JSON schemas
- Follows Medallion architecture principles
- Prepares data for Silver layer transformations

This setup forms the foundation for scalable cloud-based analytics and reporting pipelines.

