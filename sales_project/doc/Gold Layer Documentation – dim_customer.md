# Gold Layer Documentation – dim_customer

## Overview

The `dim_customer` table is a Gold Layer dimension table built using PySpark and BigQuery in a Medallion Architecture pipeline.

This dimension consolidates customer information from multiple Silver Layer sources and prepares a clean, analytics-ready customer dimension for reporting, dashboards, and fact table joins.

---

# Architecture Layer

| Layer | Purpose |
|---|---|
| Bronze | Raw source ingestion |
| Silver | Cleansed and standardized data |
| Gold | Business-ready dimensional model |

---

# Target Table

**Dataset:** `gold_sales_ds`  
**Table:** `dim_customer`

---

# Source Tables

| Source Table | Description |
|---|---|
| `silver_sales_ds.crm_customers` | CRM customer master data |
| `silver_sales_ds.erp_customer_extra` | ERP demographic details |
| `silver_sales_ds.erp_customer_loc` | ERP customer location data |

---

# Technologies Used

- PySpark 3.5.1
- Google BigQuery
- Google Cloud Storage (GCS)
- Google Colab
- Spark BigQuery Connector

---

# Spark Session Configuration

```python
spark = (
    SparkSession.builder
    .appName("GoldDimCustomer")

    .config(
        "spark.jars.packages",
        "com.google.cloud.spark:spark-3.5-bigquery:0.42.1"
    )

    .config(
        "temporaryGcsBucket",
        TEMP_BUCKET
    )

    .config(
        "parentProject",
        PROJECT_ID
    )

    .getOrCreate()
)
```

---

# Data Processing Steps

## 1. Read Silver Layer Tables

Data is loaded from BigQuery using the Spark BigQuery connector.

```python
spark.read.format("bigquery").load(TABLE_NAME)
```

---

## 2. CRM Customer Cleansing

### Operations Performed

- Selected required columns
- Removed duplicate customer IDs

### Columns Retained

- `cst_id`
- `cst_key`
- `cst_firstname`
- `cst_lastname`
- `cst_marital_status`
- `cst_gndr`
- `cst_create_date`

---

## 3. ERP Customer Extra Cleansing

### Operations Performed

- Applied window function
- Retained latest birth date per customer
- Removed duplicate rows

### Window Logic

```python
Window.partitionBy("CID").orderBy(col("BDATE").desc())
```

---

## 4. ERP Customer Location Cleansing

### Operations Performed

- Deduplicated country records
- Retained one country per customer

### Window Logic

```python
Window.partitionBy("cid").orderBy(col("CNTRY"))
```

---

# Transformation Logic

## Customer Name Standardization

Customer full name created using:

```python
concat_ws(" ", firstname, lastname)
```

Blank names replaced with:

```text
Unknown
```

---

## Marital Status Cleansing

| Original Value | Final Value |
|---|---|
| UNKNOWN | NULL |

---

## Gender Standardization

### Priority Logic

1. CRM gender used if valid
2. Otherwise ERP gender used

### Final Standardized Values

| Source Values | Final Value |
|---|---|
| M / MALE | Male |
| F / FEMALE | Female |
| NULL / UNKNOWN | Unknown |

---

## Country Mapping

Country values sourced from:

```text
erp_customer_loc
```

---

# Join Strategy

## Join Types

| Join | Type |
|---|---|
| CRM → ERP Extra | Left Join |
| CRM → ERP Location | Left Join |

---

# Performance Optimization

Broadcast joins applied for small ERP tables.

```python
broadcast(extra_df)
broadcast(loc_df)
```

## Benefits

- Reduces shuffle operations
- Improves join performance
- Optimizes Spark execution

---

# Surrogate Key Generation

A surrogate key is generated for dimensional modeling.

## Column

```text
customer_sk
```

## Method Used

```python
monotonically_increasing_id()
```

---

# Final Schema

| Column Name | Description |
|---|---|
| customer_sk | Surrogate key |
| customer_id | Business customer ID |
| customer_key | CRM customer key |
| customer_name | Full customer name |
| marital_status | Customer marital status |
| gender | Standardized gender |
| birth_date | Customer birth date |
| country | Customer country |
| customer_create_date | CRM customer creation date |

---

# Data Quality Checks

The pipeline performs:

- Duplicate removal
- Null handling
- Gender normalization
- Unknown value standardization
- Country cleansing

## Validation Example

```python
dropDuplicates(["customer_id"])
```

---

# Caching Strategy

The Gold DataFrame is cached before multiple Spark actions.

```python
gold_dim_customer.cache()
```

## Benefits

- Prevents recomputation
- Improves performance

---

# BigQuery Write Strategy

## Write Mode

```python
overwrite
```

## Destination Table

```text
gold_sales_ds.dim_customer
```

## Write Example

```python
gold_dim_customer.write \
    .format("bigquery") \
    .option(
        "table",
        "project-1928c187-e191-4e50-bee:gold_sales_ds.dim_customer"
    ) \
    .mode("overwrite") \
    .save()
```

---

# Performance Optimizations Applied

| Optimization | Purpose |
|---|---|
| Broadcast Join | Reduce shuffle |
| Cache | Avoid recomputation |
| Deduplication | Improve data quality |
| Column Pruning | Reduce memory usage |
| Left Joins | Preserve CRM customers |

---

# Recommended Future Improvements

## Replace `monotonically_increasing_id()`

Recommended alternative:

```python
row_number().over(Window.orderBy(lit(1)))
```

### Reason

- Sequential surrogate keys
- Better warehouse standards

---

## Add Partitioning

Recommended before writes:

```python
repartition(4)
```

### Benefits

- Better parallelism
- Faster writes

---

# Business Use Cases

The `dim_customer` table supports:

- Customer analytics
- Sales reporting
- Customer segmentation
- Dashboard reporting
- Fact table joins
- Star schema modeling

---

# Pipeline Flow

```text
Bronze Layer
    ↓
Silver Layer Cleansing
    ↓
Gold Dimension Creation
    ↓
BigQuery Gold Dataset
```

---

# Result

The pipeline successfully creates a clean, optimized, analytics-ready Customer Dimension table for enterprise reporting and analytics workloads.