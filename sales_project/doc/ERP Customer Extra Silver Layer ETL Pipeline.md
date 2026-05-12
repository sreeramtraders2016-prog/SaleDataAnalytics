# ERP Customer Extra Silver Layer ETL Pipeline

## Overview

This ETL pipeline processes raw ERP customer demographic data from the Bronze layer, performs cleansing, deduplication, validation, and standardization using PySpark, and loads the transformed dataset into the Silver layer in BigQuery.

The implementation follows the Medallion Architecture approach:

```text
Bronze Layer  →  Silver Layer  →  Gold Layer
 Raw Data         Clean Data      Business Analytics
```

---

# Source Table

## Bronze Layer Table

| Dataset | Table |
|---|---|
| bronze_sales_ds | erp_customer_extra_raw |

---

# Target Table

## Silver Layer Table

| Dataset | Table |
|---|---|
| silver_sales_ds | erp_customer_extra |

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

Raw ERP customer demographic data is loaded from BigQuery.

```python
df = (
    spark.read.format("bigquery").load(
        "project-1928c187-e191-4e50-bee:bronze_sales_ds.erp_customer_extra_raw"
    )
)
```

---

# 2. Customer ID Standardization

Invalid prefixes are removed from customer IDs and converted into integer format.

## Transformation

Remove the string `NASAW` from `CID`.

## Example

| Original CID | Standardized CID |
|---|---|
| NASAW11000 | 11000 |

```python
erp_cust_df = df.withColumn(
    "CID",
    regexp_replace(col("CID"), "NASAW", "").cast("int")
)
```

---

# 3. Duplicate Removal Using Window Functions

Duplicate customer records are removed using window functions.

## Logic

- Partition by `CID`
- Order by `BDATE`
- Keep the first occurrence

```python
windowSpec = Window.partitionBy("CID").orderBy("BDATE")
```

---

# 4. Row Number Assignment

A ranking column is created to identify duplicate records.

```python
row_number().over(windowSpec)
```

---

# 5. Deduplication Filtering

Only records with `rn = 1` are retained.

```python
df_dedup = erp_cust_df.withColumn(
    "rn",
    row_number().over(windowSpec)
).filter("rn = 1").drop("rn")
```

---

# 6. Birth Date Validation

Customer records are validated using business rules.

## Validation Rules

- `BDATE` cannot be NULL
- `BDATE` must not be in the future
- Customer age must be between 18 and 100 years

```python
(col("BDATE") <= current_date())
```

---

# Age Validation Formula

Customer age is calculated using the date difference.

:contentReference[oaicite:0]{index=0}

```python
(datediff(current_date(), col("BDATE")) / 365)
```

---

# 7. Date Conversion

Birth date values are converted into proper date format.

## Column

- `BDATE`

```python
to_date(col("BDATE"), "yyyy-MM-dd")
```

---

# 8. Gender Standardization

Gender values are standardized into business-readable values.

## Mapping Rules

| Source Values | Standardized Value |
|---|---|
| M, MALE | Male |
| F, FEMALE | Female |
| Blank / Other | n/a |

```python
when(
    upper(trim(col("GEN"))).isin("M", "MALE"),
    "Male"
)
```

---

# 9. Metadata Tracking

An ingestion timestamp is added for audit and lineage tracking.

```python
clean_df = clean_df.withColumn(
    "ingestion_dt",
    current_timestamp()
)
```

---

# 10. Schema Validation

The transformed schema is displayed for verification.

```python
clean_df.printSchema()
```

---

# 11. Load Data to BigQuery Silver Layer

The cleaned dataset is loaded into BigQuery.

## Current Implementation

```python
pandas_df = clean_df.toPandas()

job = client.load_table_from_dataframe(
    pandas_df,
    table_id,
    job_config=job_config
)
```

---

# Recommended Production Approach

Instead of converting Spark DataFrames into Pandas DataFrames, directly write from Spark into BigQuery for better scalability and distributed execution.

## Recommended Method

```python
clean_df.write \
    .format("bigquery") \
    .option(
        "table",
        "project-1928c187-e191-4e50-bee.silver_sales_ds.erp_customer_extra"
    ) \
    .mode("append") \
    .save()
```

---

# Final Silver Table Schema

| Column | Description |
|---|---|
| CID | Customer ID |
| BDATE | Customer Birth Date |
| GEN | Standardized Gender |
| ingestion_dt | ETL Load Timestamp |

---

# Data Quality Rules Implemented

The pipeline performs the following validations and transformations:

- Customer ID cleansing
- Duplicate removal
- Window function ranking
- Birth date validation
- Age validation
- Gender standardization
- Date conversion
- Metadata tracking

---

# Architecture Flow

```text
BigQuery Bronze Layer
        ↓
PySpark Cleansing & Validation
        ↓
BigQuery Silver Layer
        ↓
Gold Analytics Layer
```

---

# Medallion Architecture Context

## Bronze Layer
Stores raw ERP customer demographic data.

## Silver Layer
Stores validated and standardized customer demographic information.

## Gold Layer
Provides enriched customer analytics datasets and dimensional models.

---

# Business Use Cases

This Silver layer supports:

- Customer demographic analysis
- Age segmentation
- Gender-based analytics
- Customer dimension enrichment
- Regional customer insights
- BI dashboards and KPI reporting

---

# Future Improvements

- Incremental loading
- Slowly Changing Dimensions (SCD)
- Advanced demographic validation
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