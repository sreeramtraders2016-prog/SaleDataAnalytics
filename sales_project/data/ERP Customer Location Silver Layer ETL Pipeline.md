# ERP Customer Location Silver Layer ETL Pipeline

## Overview

This ETL pipeline processes raw ERP customer location data from the Bronze layer, performs cleansing, standardization, deduplication, and validation using PySpark, and loads the curated dataset into the Silver layer in BigQuery.

The implementation follows the Medallion Architecture pattern:

```text
Bronze Layer  →  Silver Layer  →  Gold Layer
 Raw Data         Clean Data      Analytics Layer
```

---

# Source Table

## Bronze Layer Table

| Dataset | Table |
|---|---|
| bronze_sales_ds | erp_customer_loc_raw |

---

# Target Table

## Silver Layer Table

| Dataset | Table |
|---|---|
| silver_sales_ds | erp_customer_loc |

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
- GCS Connector
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

Raw ERP customer location data is loaded from BigQuery.

```python
df = (
    spark.read.format("bigquery").load(
        "project-1928c187-e191-4e50-bee:bronze_sales_ds.erp_customer_loc_raw"
    )
)
```

---

# 2. Country Data Cleansing

Blank country values are converted into NULL values.

## Logic

- Trim whitespace
- Replace empty strings with NULL

```python
df_clean = df.withColumn(
    "CNTRY",
    when(trim(col("CNTRY")) == "", None)
    .otherwise(trim(col("CNTRY")))
)
```

---

# 3. Country Standardization

Country abbreviations are standardized into business-readable values.

## Mapping Rules

| Source Value | Standardized Value |
|---|---|
| US | United States |
| USA | United States |
| DE | Germany |
| UK | United Kingdom |

```python
df_clean = df_clean.replace({
    "US": "United States",
    "USA": "United States",
    "DE": "Germany",
    "UK": "United Kingdom"
}, subset=["CNTRY"])
```

---

# 4. Customer ID Standardization

Special characters are removed from customer identifiers.

## Transformation

Remove hyphens (`-`) from `CID`.

## Example

| Original CID | Standardized CID |
|---|---|
| AW-00011000 | AW00011000 |

```python
regexp_replace(col("CID"), "-", "")
```

---

# 5. Duplicate Removal

Duplicate customer location records are removed using window functions.

## Logic

- Partition by `CID`
- Retain only the first occurrence

```python
window_spec = Window.partitionBy("CID").orderBy("CID")
```

## Ranking

```python
row_number().over(window_spec)
```

---

# 6. Deduplication Filtering

Only records with row number = 1 are retained.

```python
df_dedup = df_dedup.filter(col("rn") == 1)
```

Temporary helper columns are removed after processing.

---

# 7. Metadata Tracking

An ingestion timestamp is added for audit and lineage tracking.

```python
df_dedup = df_dedup.withColumn(
    "ingestion_dt",
    current_timestamp()
)
```

---

# 8. Validation Check

Distinct country values are displayed for validation.

```python
df_dedup.select("CNTRY").distinct().show()
```

---

# 9. Load Data to BigQuery Silver Layer

The transformed dataset is loaded into BigQuery.

## Current Implementation

```python
pandas_df = df_dedup.toPandas()

job = client.load_table_from_dataframe(
    pandas_df,
    table_id,
    job_config=job_config
)
```

---

# Recommended Production Approach

Instead of converting Spark DataFrames to Pandas, write directly from Spark to BigQuery for improved scalability and distributed processing.

## Recommended Method

```python
df_dedup.write \
    .format("bigquery") \
    .option(
        "table",
        "project-1928c187-e191-4e50-bee.silver_sales_ds.erp_customer_loc"
    ) \
    .mode("append") \
    .save()
```

---

# Final Silver Table Schema

| Column | Description |
|---|---|
| CID | Standardized Customer ID |
| CNTRY | Standardized Country Name |
| ingestion_dt | ETL Load Timestamp |

---

# Data Quality Rules Implemented

The pipeline applies the following validations and transformations:

- Blank value handling
- Country standardization
- Customer ID cleansing
- Duplicate removal
- Window function deduplication
- Metadata tracking
- Validation checks

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
Stores raw ERP customer location data.

## Silver Layer
Stores validated and standardized customer location information.

## Gold Layer
Provides enriched dimensional customer analytics datasets.

---

# Business Use Cases

This Silver layer supports:

- Customer geography analysis
- Regional sales reporting
- Country-level KPI dashboards
- Customer segmentation
- Geographic enrichment for customer dimensions

---

# Future Improvements

- Incremental loading
- Country validation using reference tables
- ISO country code standardization
- Data quality monitoring
- Logging framework
- Partitioned BigQuery tables
- Airflow orchestration

---

# Author

Srinivas Palika

---

# Project

Sales Data Analytics Engineering Project