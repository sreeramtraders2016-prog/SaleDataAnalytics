# CRM Customers Silver Layer ETL Pipeline

## Overview

This ETL pipeline processes raw CRM customer data from the Bronze layer, performs cleansing and standardization using PySpark, and loads the transformed data into the Silver layer in BigQuery.

The solution follows the Medallion Architecture approach:

```text
Bronze Layer  →  Silver Layer  →  Gold Layer
 Raw Data         Clean Data      Analytics Layer
```

---

# Source Table

## Bronze Layer Table

| Dataset | Table |
|---|---|
| bronze_sales_ds | crm_customers_raw |

---

# Target Table

## Silver Layer Table

| Dataset | Table |
|---|---|
| silver_sales_ds | crm_customers |

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
- Temporary Cloud Storage Bucket
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

Customer raw data is loaded from BigQuery Bronze layer.

```python
df = (
    spark.read.format("bigquery")
    .load(
        "project-1928c187-e191-4e50-bee:bronze_sales_ds.crm_customers_raw"
    )
)
```

---

# 2. Null Handling

Rows with missing customer IDs are removed.

## Validated Column

- `cst_id`

```python
clean_df = df.na.drop(subset=["cst_id"])
```

---

# 3. Duplicate Removal

Duplicate customer records are removed using the customer ID.

```python
clean_df = clean_df.dropDuplicates(["cst_id"])
```

---

# 4. Data Type Standardization

Customer ID is converted into integer type.

```python
clean_df = clean_df.withColumn(
    "cst_id",
    col("cst_id").cast("int")
)
```

---

# 5. String Cleaning

Whitespace is removed from text columns.

## Columns Trimmed

- `cst_key`
- `cst_firstname`
- `cst_lastname`
- `cst_marital_status`
- `cst_gndr`

```python
trim(col(c))
```

---

# 6. Date Conversion

Customer creation date is converted into proper date format.

## Column

- `cst_create_date`

```python
to_date("cst_create_date", "yyyy-MM-dd")
```

---

# 7. Gender Standardization

Customer gender values are standardized into readable business values.

## Mapping Rules

| Source Value | Standardized Value |
|---|---|
| M | Male |
| F | Female |
| NULL / Other | Unknown |

```python
when(
    upper(col("cst_gndr")) == "M",
    "Male"
)
```

---

# 8. Marital Status Standardization

Marital status values are standardized.

## Mapping Rules

| Source Value | Standardized Value |
|---|---|
| M | Married |
| S | Single |
| NULL / Other | Unknown |

```python
when(
    upper(col("cst_marital_status")) == "M",
    "Married"
)
```

---

# 9. Data Preview

The cleaned dataset is displayed for validation.

```python
clean_df.show(5)
```

---

# 10. Null Validation Check

A null analysis is performed across all columns.

```python
clean_df.select([
    sum(col(c).isNull().cast("int")).alias(c)
    for c in clean_df.columns
]).show()
```

---

# 11. Load Data into BigQuery Silver Layer

The transformed Spark DataFrame is loaded into BigQuery.

## Current Implementation

```python
pandas_df = clean_df.toPandas()

client = bigquery.Client(project=PROJECT_ID)

job = client.load_table_from_dataframe(
    pandas_df,
    table_id,
    job_config=job_config
)
```

---

# Recommended Production Approach

Instead of converting Spark DataFrames to Pandas, write directly from Spark into BigQuery for better scalability and performance.

## Recommended Method

```python
clean_df.write \
    .format("bigquery") \
    .option(
        "table",
        "project-1928c187-e191-4e50-bee.silver_sales_ds.crm_customers"
    ) \
    .mode("append") \
    .save()
```

---

# Final Silver Table Schema

| Column | Description |
|---|---|
| cst_id | Customer ID |
| cst_key | Customer Business Key |
| cst_firstname | Customer First Name |
| cst_lastname | Customer Last Name |
| cst_marital_status | Standardized Marital Status |
| cst_gndr | Standardized Gender |
| cst_create_date | Customer Creation Date |

---

# Data Quality Rules Implemented

The pipeline includes the following validations:

- Null handling
- Duplicate removal
- String trimming
- Type casting
- Gender standardization
- Marital status standardization
- Date conversion
- Null auditing

---

# Architecture Flow

```text
BigQuery Bronze Layer
        ↓
PySpark Data Cleansing
        ↓
BigQuery Silver Layer
        ↓
Gold Analytics Layer
```

---

# Medallion Architecture Context

## Bronze Layer
Contains raw ingested CRM data.

## Silver Layer
Contains cleaned, validated, and standardized customer data.

## Gold Layer
Contains business-ready analytical models and KPIs.

---

# Future Improvements

- Incremental data loading
- Slowly Changing Dimensions (SCD Type 2)
- Data quality monitoring
- Logging and error handling
- Partitioned BigQuery tables
- Workflow orchestration using Airflow
- Data catalog integration

---

# Author

Srinivas Palika

---

# Project

Sales Data Analytics Engineering Project