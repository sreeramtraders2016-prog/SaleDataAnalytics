# CRM Sales Silver Layer ETL Pipeline

## Overview

This ETL pipeline processes raw CRM sales transaction data from the Bronze layer, performs cleansing, validation, transformation, and quality checks using PySpark, and loads the curated data into the Silver layer in BigQuery.

The solution follows the Medallion Architecture approach:

```text
Bronze Layer  →  Silver Layer  →  Gold Layer
 Raw Data         Clean Data      Business Analytics
```

---

# Source Table

## Bronze Layer Table

| Dataset | Table |
|---|---|
| bronze_sales_ds | crm_sales_raw |

---

# Target Table

## Silver Layer Table

| Dataset | Table |
|---|---|
| silver_sales_ds | crm_sales |

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

Sales transaction data is loaded from BigQuery Bronze layer.

```python
df = (
    spark.read.format("bigquery")
    .load(
        "project-1928c187-e191-4e50-bee:bronze_sales_ds.crm_sales_raw"
    )
)
```

---

# 2. Deduplication Using Window Functions

Duplicate sales orders are identified and removed using window functions.

## Logic

- Partition by `sls_ord_num`
- Keep the latest order record based on `sls_order_dt`

```python
window_spec = Window.partitionBy("sls_ord_num") \
                    .orderBy(col("sls_order_dt").desc())

df_ranked = df.withColumn(
    "row_num",
    row_number().over(window_spec)
)
```

Only records with `row_num = 1` are retained.

---

# 3. String Cleaning

Whitespace is removed from string columns.

## Columns Trimmed

- `sls_ord_num`
- `sls_prd_key`

```python
trim(col("sls_ord_num"))
```

---

# 4. Data Type Standardization

Columns are converted into appropriate data types.

## Type Conversions

| Column | Data Type |
|---|---|
| sls_quantity | Integer |
| sls_price | Float |
| sls_sales | Float |

```python
col("sls_price").cast("float")
```

---

# 5. Date Conversion

Integer/string date columns are converted into proper date format.

## Date Columns

- `sls_order_dt`
- `sls_ship_dt`
- `sls_due_dt`

## Source Format

```text
yyyyMMdd
```

## Transformation

```python
to_date(col(c).cast("string"), "yyyyMMdd")
```

---

# 6. Sales Amount Validation

A calculated sales amount column is generated.

## Formula

```text
sls_sales_calc = sls_quantity × sls_price
```

```python
df_ranked = df_ranked.withColumn(
    "sls_sales_calc",
    col("sls_quantity") * col("sls_price")
)
```

---

# 7. Metadata Column

An ingestion timestamp is added for audit tracking.

```python
df_ranked = df_ranked.withColumn(
    "ingestion_dt",
    current_timestamp()
)
```

---

# 8. Data Quality Validation

Sales records are validated against calculated sales values.

## Validation Rule

```text
sls_sales == sls_sales_calc
```

---

# Valid Records

```python
valid_df = df_ranked.withColumn(
    "sales_mismatch",
    col("sls_sales") == col("sls_sales_calc")
)
```

---

# Invalid Records

```python
invalid_df = df_ranked.withColumn(
    "sales_mismatch",
    col("sls_sales") != col("sls_sales_calc")
)
```

---

# 9. Remove Temporary Columns

The ranking helper column is removed.

```python
df_ranked = df_ranked.drop("row_num")
```

---

# 10. Schema Validation

The transformed schema is printed for verification.

```python
df_ranked.printSchema()
```

---

# 11. Load Data to BigQuery Silver Layer

The transformed dataset is loaded into BigQuery.

## Current Implementation

```python
pandas_df = df_ranked.toPandas()

job = client.load_table_from_dataframe(
    pandas_df,
    table_id,
    job_config=job_config
)
```

---

# Recommended Production Approach

Instead of converting Spark DataFrames into Pandas DataFrames, directly write from Spark into BigQuery.

## Recommended Method

```python
df_ranked.write \
    .format("bigquery") \
    .option(
        "table",
        "project-1928c187-e191-4e50-bee.silver_sales_ds.crm_sales"
    ) \
    .mode("append") \
    .save()
```

---

# Final Silver Table Schema

| Column | Description |
|---|---|
| sls_ord_num | Sales Order Number |
| sls_prd_key | Product Key |
| sls_cust_id | Customer ID |
| sls_order_dt | Order Date |
| sls_ship_dt | Ship Date |
| sls_due_dt | Due Date |
| sls_sales | Sales Amount |
| sls_quantity | Quantity Sold |
| sls_price | Product Price |
| sls_sales_calc | Calculated Sales Amount |
| ingestion_dt | ETL Load Timestamp |

---

# Data Quality Rules Implemented

The pipeline performs the following validations:

- Duplicate removal
- String trimming
- Data type casting
- Date conversion
- Sales amount validation
- Schema validation
- Audit metadata tracking

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
Stores raw ingested CRM sales transactions.

## Silver Layer
Stores validated and standardized sales transaction data.

## Gold Layer
Stores business-ready aggregated datasets and KPIs.

---

# Business Use Cases

The Silver sales dataset supports:

- Revenue analysis
- Order trend analysis
- Customer purchasing behavior
- Product performance analysis
- Sales forecasting
- KPI dashboards
- Fact table generation

---

# Future Improvements

- Incremental loading
- Partitioned BigQuery tables
- Slowly Changing Dimensions (SCD)
- Data quality monitoring
- Error logging framework
- Workflow orchestration using Airflow
- Real-time streaming integration

---

# Author

Srinivas Palika

---

# Project

Sales Data Analytics Engineering Project