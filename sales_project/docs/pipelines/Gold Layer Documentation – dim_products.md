# Gold Layer Documentation – dim_products

## Overview

The `dim_products` table is a Gold Layer dimension table built using PySpark and BigQuery within a Medallion Architecture pipeline.

This table combines CRM product data with ERP product category information to create a clean, analytics-ready product dimension for reporting, dashboards, and fact table joins.

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
**Table:** `dim_products`

---

# Source Tables

| Source Table | Description |
|---|---|
| `silver_sales_ds.crm_products` | CRM product master data |
| `silver_sales_ds.erp_product_category` | ERP product category details |

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
    .appName("GoldDimProducts")

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

    # PERFORMANCE
    .config("spark.sql.shuffle.partitions", "8")
    .config("spark.default.parallelism", "8")

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

## 2. Remove Duplicate ERP Product Categories

Duplicate category IDs are removed before joining.

```python
pc_clean = (
    erp_product_category_df
    .dropDuplicates(["ID"])
)
```

### Purpose

- Prevent duplicate join results
- Improve data quality
- Avoid Cartesian duplication

---

# Join Strategy

## Join Type

| Join | Type |
|---|---|
| CRM Products → ERP Product Category | Left Join |

---

## Broadcast Join Optimization

Small ERP category table is broadcasted.

```python
broadcast(pc)
```

### Benefits

- Reduces shuffle operations
- Improves join performance
- Optimizes Spark execution

---

# Transformation Logic

## Product Name Mapping

CRM product name mapped as:

```python
col("prd.prd_nm").alias("product_name")
```

---

## Product Cost Mapping

CRM product cost mapped as:

```python
col("prd.prd_cost").alias("product_cost")
```

---

## Product Category Mapping

ERP category fields mapped as:

| ERP Column | Gold Column |
|---|---|
| CAT | product_cat |
| SUBCAT | product_sub_cat |

---

## Maintenance Indicator

Maintenance field retained directly from ERP data.

```python
col("pc.MAINTENANCE")
```

---

# Surrogate Key Generation

A surrogate key is generated for dimensional modeling.

## Column

```text
product_sk
```

## Method Used

```python
monotonically_increasing_id()
```

---

# Final Schema

| Column Name | Description |
|---|---|
| product_sk | Surrogate key |
| prd_id | Product business ID |
| prd_key | Product key |
| product_name | Product name |
| product_cost | Product cost |
| product_line | Product line |
| product_cat | Product category |
| product_sub_cat | Product subcategory |
| MAINTENANCE | Maintenance indicator |
| prd_start_dt | Product start date |
| prd_end_dt | Product end date |

---

# Performance Optimizations Applied

| Optimization | Purpose |
|---|---|
| Broadcast Join | Reduce shuffle |
| Persist Cache | Avoid recomputation |
| Repartition | Parallelize writes |
| Column Pruning | Reduce memory usage |
| Deduplication | Improve data quality |

---

# Persistence Strategy

The DataFrame is persisted using:

```python
StorageLevel.MEMORY_AND_DISK
```

Example:

```python
product_dim_df.persist(StorageLevel.MEMORY_AND_DISK)
```

### Benefits

- Prevents lineage recomputation
- Handles large datasets safely
- Improves repeated action performance

---

# Repartitioning Strategy

Before writing output:

```python
product_dim_df = product_dim_df.repartition(4)
```

### Benefits

- Improves parallelism
- Optimizes distributed writes
- Reduces small file issues

---

# CSV Output Strategy

## Output Path

```text
/content/gold_dim_products_csv
```

---

## CSV Write Configuration

```python
(
    product_dim_df.write
    .mode("overwrite")
    .option("header", True)
    .option("compression", "snappy")
    .csv(output_path)
)
```

---

# Compression

Compression used:

```text
snappy
```

### Benefits

- Faster read/write performance
- Reduced storage size
- Optimized distributed processing

---

# Optional Single CSV Export

```python
product_dim_df.coalesce(1).write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("/content/gold_dim_products_single_csv")
```

### Purpose

- Generates one CSV file
- Useful for downloads or demos

### Tradeoff

- Slower for large datasets
- Reduces parallelism

---

# Optional BigQuery Write

```python
product_dim_df.write \
    .format("bigquery") \
    .option(
        "table",
        "project-1928c187-e191-4e50-bee.gold_sales_ds.dim_products"
    ) \
    .mode("overwrite") \
    .save()
```

---

# Data Quality Controls

The pipeline performs:

- Duplicate removal
- Column standardization
- Controlled joins
- Consistent schema generation

---

# Business Use Cases

The `dim_products` table supports:

- Product analytics
- Sales reporting
- Product hierarchy analysis
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
Gold Product Dimension Creation
    ↓
CSV / BigQuery Output
```

---

# Result

The pipeline successfully creates a clean, optimized, analytics-ready Product Dimension table for enterprise analytics and reporting workloads.