# CRM Products Silver Layer ETL Pipeline

## Overview

This pipeline processes raw CRM product data from the Bronze layer, performs data cleaning and transformation using PySpark, and loads the curated data into the Silver layer in BigQuery.

The ETL workflow follows the Medallion Architecture pattern:

```text
Bronze Layer  →  Silver Layer  →  Gold Layer
 Raw Data         Clean Data      Business Analytics
```

---

# Source Table

## Bronze Table

| Dataset | Table |
|---|---|
| bronze_sales_ds | crm_products_raw |

---

# Target Table

## Silver Table

| Dataset | Table |
|---|---|
| silver_sales_ds | crm_products |

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

- BigQuery connector
- Google Cloud Storage connector
- Temporary GCS bucket
- Project configuration

```python
spark = (
    SparkSession.builder
    .appName("BigQueryIntegration")
)
```

---

# Data Processing Steps

## 1. Read Bronze Data

The raw CRM product data is loaded from BigQuery.

```python
df = (
    spark.read.format("bigquery")
    .load(
        "project-1928c187-e191-4e50-bee:bronze_sales_ds.crm_products_raw"
    )
)
```

---

# 2. Null Handling

Records with missing critical keys are removed.

## Columns Validated

- `prd_id`
- `prd_key`

```python
clean_df = df.na.drop(
    subset=["prd_id", "prd_key"]
)
```

---

# 3. Product Category Key Extraction

A category identifier (`cid`) is extracted from the product key.

## Example

| Original prd_key | Extracted cid |
|---|---|
| CO-DE-RD-2308 | CO_DE |

```python
clean_df = clean_df.withColumn(
    "cid",
    regexp_replace(
        substring(col("prd_key"), 1, 5),
        "-",
        "_"
    )
)
```

---

# 4. Product Key Standardization

The product key is cleaned and reformatted.

## Example

| Original | Standardized |
|---|---|
| CO-DE-RD-2308 | RD_2308 |

```python
clean_df = clean_df.withColumn(
    "prd_key",
    regexp_replace(
        expr("substring(prd_key, 7)"),
        "-",
        "_"
    )
)
```

---

# 5. Trim String Columns

Whitespace is removed from text columns.

## Columns Cleaned

- `prd_key`
- `prd_nm`
- `prd_line`

```python
trim(col(c))
```

---

# 6. Data Type Casting

## Transformations

| Column | Data Type |
|---|---|
| prd_id | Integer |
| prd_cost | Float |

```python
col("prd_cost").cast("float")
```

---

# 7. Product Cost Validation

Invalid product costs are removed.

## Rules

- Cost cannot be NULL
- Cost must be greater than or equal to 0

```python
clean_df = clean_df.filter(
    col("prd_cost") >= 0
)
```

---

# 8. Product Line Standardization

Product line abbreviations are converted into readable business values.

## Mapping Rules

| Source | Standardized |
|---|---|
| M | Mountain |
| R | Road |
| S | Standard |
| T | Touring |
| NULL/Other | Unknown |

```python
when(
    upper(trim(col("prd_line"))) == "M",
    "Mountain"
)
```

---

# 9. Date Conversion

Date columns are converted into proper date format.

## Columns

- `prd_start_dt`
- `prd_end_dt`

```python
to_date(col("prd_start_dt"), "yyyy-MM-dd")
```

---

# 10. Date Validation

Records with invalid date ranges are removed.

## Validation Rules

- `prd_start_dt` cannot be NULL
- `prd_end_dt` must be greater than or equal to `prd_start_dt`

```python
col("prd_start_dt") <= col("prd_end_dt")
```

---

# 11. Metadata Column

An ingestion timestamp is added for audit tracking.

```python
clean_df = clean_df.withColumn(
    "ingestion_dt",
    current_timestamp()
)
```

---

# 12. Load Data to Silver Layer

The cleaned Spark DataFrame is written directly into BigQuery.

```python
clean_df.write \
    .format("bigquery") \
    .option(
        "table",
        "project-1928c187-e191-4e50-bee.silver_sales_ds.crm_products"
    ) \
    .mode("overwrite") \
    .save()
```

---

# Final Silver Table Schema

| Column | Description |
|---|---|
| prd_id | Product ID |
| cid | Product Category ID |
| prd_key | Standardized Product Key |
| prd_nm | Product Name |
| prd_cost | Product Cost |
| prd_line | Product Line |
| prd_start_dt | Product Start Date |
| prd_end_dt | Product End Date |
| ingestion_dt | ETL Load Timestamp |

---

# Data Quality Checks

The pipeline implements the following validations:

- Null handling
- Duplicate prevention
- Type casting
- String trimming
- Product line standardization
- Cost validation
- Date validation
- Metadata tracking

---

# Architecture Flow

```text
BigQuery Bronze Layer
        ↓
PySpark Transformation
        ↓
BigQuery Silver Layer
        ↓
Gold Analytics Layer
```

---

# Future Enhancements

- Incremental loading
- Slowly Changing Dimensions (SCD)
- Data quality monitoring
- Logging framework
- Partitioned BigQuery tables
- Automated orchestration using Airflow

---

# Author

Srinivas Palika

---

# Project

Sales Data Analytics Engineering Project