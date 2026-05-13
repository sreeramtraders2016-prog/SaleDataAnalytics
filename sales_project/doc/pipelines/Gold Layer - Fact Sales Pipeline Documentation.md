# Gold Layer - Fact Sales Pipeline Documentation

## Overview

This pipeline creates the `fact_sales` table in the Gold Layer using PySpark.

The process integrates:

- CRM sales transactions
- Product dimension
- Customer dimension

The final dataset supports:

- BI reporting
- Sales analytics
- Star schema modeling
- Data warehouse querying

---

# Architecture Flow

```text
CRM Sales (Silver)
        |
        v
Product Dimension (Gold)
        |
        v
Customer Dimension (Gold)
        |
        v
Fact Sales Table (Gold)
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| PySpark 3.5.1 | Distributed data processing |
| Google BigQuery | Cloud data warehouse |
| Google Colab | Execution environment |
| GCS Bucket | Temporary Spark staging |

---

# Source Tables

## Silver Layer

| Table | Description |
|---|---|
| `silver_sales_ds.crm_sales` | Sales transactions |

---

## Gold Layer Dimensions

| File | Description |
|---|---|
| `gold_dim_products.csv` | Product dimension |
| `gold_dim_customers.csv` | Customer dimension |

---

# Pipeline Steps

# 1. Create Spark Session

Spark session is configured with:

- BigQuery connector
- Parent project
- Temporary GCS bucket

## Code

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

# 2. Read CRM Sales Data

Sales transactions are loaded from BigQuery.

## Code

```python
crm_sales_df = (
    spark.read.format("bigquery")
    .load(
        "project-1928c187-e191-4e50-bee:silver_sales_ds.crm_sales"
    )
)
```

---

# 3. Standardize Product Keys

Hyphens are replaced with underscores to ensure successful joins with the product dimension.

## Example

| Before | After |
|---|---|
| `WB-H098` | `WB_H098` |
| `BK-R79Y-44` | `BK_R79Y_44` |

## Code

```python
crm_sales_df = crm_sales_df.withColumn(
    "sls_prd_key",
    regexp_replace("sls_prd_key","-","_" )
)
```

---

# 4. Read Product Dimension

Product dimension CSV is loaded.

## Code

```python
dim_products_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/content/gold_dim_products.csv")
)
```

---

# 5. Filter Active Products

Only active products are retained.

## Active Product Logic

A product is active when:

- `prd_end_dt IS NULL`
OR
- `prd_end_dt >= current_date()`

## Code

```python
active_products_df = dim_products_df.filter(
    (col("prd_end_dt").isNull()) |
    (col("prd_end_dt") >= current_date())
)
```

---

# 6. Read Customer Dimension

Customer dimension CSV is loaded.

## Code

```python
dim_customers_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("/content/gold_dim_customers.csv")
)
```

---

# 7. Create Fact Sales Table

Sales data is joined with:

- Product dimension
- Customer dimension

## Join Conditions

| Join | Condition |
|---|---|
| Sales → Products | `sls_prd_key = prd_key` |
| Sales → Customers | `sls_cust_id = customer_id` |

## Code

```python
fact_sales_df = (
    crm_sales_df.alias("s")

    .join(
        dim_products_df.alias("p"),
        col("s.sls_prd_key") == col("p.prd_key"),
        "left"
    )

    .join(
        dim_customers_df.alias("c"),
        col("s.sls_cust_id") == col("c.customer_id"),
        "left"
    )
)
```

---

# 8. Handle Missing Prices

If `sls_price` is null:

- Replace with `product_cost`

## Code

```python
fact_sales_df = fact_sales_df.withColumn(
    "sls_price",
    coalesce(col("sls_price"), col("product_cost"))
)
```

---

# 9. Detect Return Transactions

Negative prices indicate return transactions.

## Code

```python
fact_sales_df = fact_sales_df.withColumn(
    "is_return",
    when(col("sls_price") < 0, 1).otherwise(0)
)
```

---

# 10. Final Fact Table Columns

## Selected Columns

| Column | Description |
|---|---|
| `sls_ord_num` | Sales order number |
| `sls_order_dt` | Order date |
| `sls_ship_dt` | Ship date |
| `sls_due_dt` | Due date |
| `customer_sk` | Customer surrogate key |
| `product_sk` | Product surrogate key |
| `sls_sales` | Sales amount |
| `sls_quantity` | Quantity sold |
| `sls_price` | Unit price |
| `sls_sales_calc` | Calculated sales amount |

## Code

```python
fact_sales_final = fact_sales_df.select(
    "sls_ord_num",
    "sls_order_dt",
    "sls_ship_dt",
    "sls_due_dt",

    "customer_sk",
    "product_sk",

    "sls_sales",
    "sls_quantity",
    "sls_price",
    "sls_sales_calc"
)
```

---

# 11. Write Output to CSV

The final fact table is written as CSV.

## Code

```python
fact_sales_final.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("/content/gold_fact_sales")
```

---

# Optional BigQuery Load

## Code

```python
fact_sales_final.write \
    .format("bigquery") \
    .option(
        "table",
        "project-1928c187-e191-4e50-bee.gold_sales_ds.fact_sales"
    ) \
    .mode("overwrite") \
    .save()
```

---

# Performance Optimizations

| Optimization | Purpose |
|---|---|
| Column pruning | Reads only required columns |
| Left joins | Preserves all sales transactions |
| CSV partitioning | Improves write performance |
| Product key standardization | Prevents join mismatches |
| Active product filtering | Reduces unnecessary records |

---

# Data Quality Checks

## Product Key Validation

Ensures:

- Sales keys match product dimension keys

---

## Null Handling

| Column | Handling |
|---|---|
| `sls_price` | Replaced with product cost |
| `prd_end_dt` | Null means active product |

---

## Return Detection

Negative prices are flagged as return transactions.

---

# Sample Output

| sls_ord_num | customer_sk | product_sk | sls_sales |
|---|---|---|---|
| SO51259 | 1297080123394 | 137 | 10.0 |
| SO51298 | 627065225304 | 137 | 25.0 |
| SO51387 | 644245094405 | 125 | 70.0 |

---

# Final Result

The pipeline successfully creates a scalable Gold Layer fact table that:

- Supports dimensional modeling
- Enables analytical reporting
- Improves query performance
- Standardizes joins across datasets
- Supports enterprise data warehousing