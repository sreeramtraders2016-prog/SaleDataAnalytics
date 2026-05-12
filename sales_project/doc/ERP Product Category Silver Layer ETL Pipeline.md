# ERP Product Category Silver Layer ETL Pipeline

## Overview

This ETL pipeline processes raw ERP product category data from the Bronze layer, performs cleansing, standardization, null validation, deduplication, and transformation using PySpark, and loads the curated dataset into the Silver layer in BigQuery.

The implementation follows the Medallion Architecture pattern:

```text
Bronze Layer  →  Silver Layer  →  Gold Layer
 Raw Data         Clean Data      Business Analytics
```

---

# Source Table

## Bronze Layer Table

| Dataset | Table |
|---|---|
| bronze_sales_ds | erp_product_category_raw |

---

# Target Table

## Silver Layer Table

| Dataset | Table |
|---|---|
| silver_sales_ds | erp_product_category |

---

# Technologies Used

- Google Colab
- PySpark 3.5.1
- Google BigQuery
- Google Cloud Storage
- Spark BigQuery Connector

---

# Spark Session Configuration

The Spark session is configured with:

- BigQuery Connector
- Google Cloud Storage Connector
- Temporary GCS Bucket
- Parent Project Configuration

```python
spark = (
    SparkSession.builder
    .appName("BigQueryIntegration")
)
```

---

# ETL Processing Steps

# 1. Read Bronze Layer Data

Raw ERP product category data is loaded from BigQuery.

```python
df = (
    spark.read.format("bigquery").load(
        "project-1928c187-e191-4e50-bee:bronze_sales_ds.erp_product_category_raw"
    )
)
```

---

# 2. String Cleaning

Whitespace is removed from all important business columns.

## Columns Trimmed

- `ID`
- `CAT`
- `SUBCAT`
- `MAINTENANCE`

```python
trim(col("ID"))
```

---

# 3. Metadata Tracking

An ingestion timestamp is added for audit and lineage tracking.

```python
df = df.withColumn(
    "ingestion_dt",
    current_timestamp()
)
```

---

# 4. Data Preview

The transformed dataset is displayed for validation.

```python
df.show()
```

---

# 5. Null Validation Check

A null analysis is performed across all columns.

```python
df.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in df.columns
]).show()
```

---

# 6. Duplicate Removal Using Window Functions

Duplicate product category records are removed using window functions.

## Logic

- Partition by `ID`
- Keep the first occurrence

```python
window_spec = Window.partitionBy("ID").orderBy("ID")
```

---

# 7. Row Number Assignment

A ranking column is generated to identify duplicates.

```python
df = df.withColumn(
    "rn",
    row_number().over(window_spec)
)
```

---

# 8. Deduplication Filtering

Only records with `rn = 1` are retained.

```python
df = df.filter(col("rn") == 1).drop("rn")
```

Temporary helper columns are removed after processing.

---

# 9. Load Data to BigQuery Silver Layer

The transformed dataset is loaded into BigQuery.

## Current Implementation

```python
pandas_df = df.toPandas()

job = client.load_table_from_dataframe(
    pandas_df,
    table_id,
    job_config=job_config
)
```

---

# Recommended Production Approach

Instead of converting Spark DataFrames to Pandas, directly write from Spark into BigQuery for scalable distributed processing.

## Recommended Method

```python
df.write \
    .format("bigquery") \
    .option(
        "table",
        "project-1928c187-e191-4e50-bee.silver_sales_ds.erp_product_category"
    ) \
    .mode("append") \
    .save()
```

---

# Final Silver Table Schema

| Column | Description |
|---|---|
| ID | Product Category ID |
| CAT | Product Category |
| SUBCAT | Product Subcategory |
| MAINTENANCE | Maintenance Indicator |
| ingestion_dt | ETL Load Timestamp |

---

# Data Quality Rules Implemented

The pipeline applies the following validations and transformations:

- String trimming
- Null validation
- Duplicate removal
- Window function ranking
- Metadata tracking
- Validation preview

---

# Architecture Flow

```text
BigQuery Bronze Layer
        ↓
PySpark Cleansing & Standardization
        ↓
BigQuery Silver Layer
        ↓
Gold Analytics Layer
```

---

# Medallion Architecture Context

## Bronze Layer
Stores raw ERP product category data.

## Silver Layer
Stores validated and standardized product category information.

## Gold Layer
Provides enriched dimensional product analytics datasets.

---

# Business Use Cases

This Silver layer supports:

- Product hierarchy analysis
- Product categorization
- Maintenance reporting
- Product dimension enrichment
- Sales category analytics
- KPI dashboards

---

# Future Improvements

- Incremental loading
- Product hierarchy validation
- Reference table integration
- Data quality monitoring
- Logging framework
- Partitioned BigQuery tables
- Workflow orchestration using Airflow

---

# Author

Srinivas Palika

---

# Project

Sales Data Analytics Engineering Project