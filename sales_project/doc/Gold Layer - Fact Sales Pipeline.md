# Gold Layer - Fact Sales Pipeline

## Overview

This pipeline creates the `fact_sales` table in the Gold Layer using PySpark.

The process combines:

- CRM Sales transactional data
- Gold Product Dimension
- Gold Customer Dimension

The final output is a star-schema fact table optimized for analytics and reporting.

---

# Architecture Flow

CRM Sales
↓
Gold Product Dimension
↓
Gold Customer Dimension
↓
Fact Sales Table

---

# Technologies Used

| Technology | Purpose |
|---|---|
| PySpark 3.5.1 | Distributed data processing |
| Google BigQuery | Data warehouse |
| Google Colab | Execution environment |
| GCS Temporary Bucket | Spark-BigQuery connector staging |

---

# Source Tables

## Silver Layer

| Table | Description |
|---|---|
| `silver_sales_ds.crm_sales` | Raw sales transactions |

---

## Gold Layer Dimensions

| Table/File | Description |
|---|---|
| `gold_dim_products.csv` | Product dimension |
| `gold_dim_customers.csv` | Customer dimension |

---

# Pipeline Steps

## 1. Initialize Spark Session

Spark session is configured with:

- BigQuery connector
- Temporary GCS bucket
- Parent project

Additional settings improve distributed execution.

---

## 2. Read CRM Sales Data

Sales data is loaded from BigQuery:

```python
crm_sales_df = (
    spark.read.format("bigquery")
    .load(
        "project-1928c187-e191-4e50-bee:silver_sales_ds.crm_sales"
    )
)