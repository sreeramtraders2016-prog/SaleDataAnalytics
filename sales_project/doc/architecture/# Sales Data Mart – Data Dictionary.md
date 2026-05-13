# Sales Data Mart – Data Dictionary

## Project Overview

This document defines the structure, business meaning, validations, and example values for the Gold Layer star schema tables:

- dim_customers
- dim_products
- fact_sales

The data mart follows a Star Schema architecture for analytical reporting and business intelligence.

---

# 1. Dimension Table: dim_customers

## Purpose

Stores customer master data used for customer analytics and reporting.

## Table Grain

One record per customer.

## Primary Key

customer_sk

---

## Column Definitions

| Column Name | Data Type | Description | Example Value | Validation Rules |
|---|---|---|---|---|
| customer_sk | BIGINT | Surrogate key generated in Gold layer | 1297080123394 | Must be unique and not null |
| customer_id | INT | Original CRM customer ID | 11433 | Must be unique |
| customer_key | STRING | CRM business customer key | AW00011433 | Cannot be null |
| customer_name | STRING | Full customer name | Maurice Shan | Default to 'Unknown' if blank |
| marital_status | STRING | Customer marital status | Married | Allowed: Married, Single, Unknown |
| gender | STRING | Standardized gender value | Male | Allowed: Male, Female, Unknown |
| birth_date | DATE | Customer birth date | 1957-03-01 | Must be valid date |
| country | STRING | Customer country | France | Country value standardized |
| customer_create_date | DATE | CRM customer creation date | 2025-10-08 | Cannot be future date |

---

## Sample Record

```text
customer_sk           : 1297080123394
customer_id           : 11433
customer_key          : AW00011433
customer_name         : Maurice Shan
marital_status        : Married
gender                : Male
birth_date            : 1957-03-01
country               : France
customer_create_date  : 2025-10-08
```

---

## Business Rules

- Duplicate customers removed using:
  
```python
dropDuplicates(["customer_id"])
```

- Gender standardized using mapping logic:
  - M → Male
  - F → Female
  - NULL → Unknown

- Empty names converted to:
  
```text
Unknown
```

---

# 2. Dimension Table: dim_products

## Purpose

Stores product master and product category information.

## Table Grain

One record per product.

## Primary Key

product_sk

---

## Column Definitions

| Column Name | Data Type | Description | Example Value | Validation Rules |
|---|---|---|---|---|
| product_sk | BIGINT | Surrogate product key | 137 | Must be unique |
| prd_id | INT | Original product ID | 477 | Cannot be null |
| prd_key | STRING | Product business key | WB_H098 | Must be standardized |
| product_name | STRING | Product name | Water Bottle - 30 oz. | Cannot be blank |
| product_cost | DOUBLE | Product standard cost | 2.0 | Must be >= 0 |
| product_line | STRING | Product line | Standard | Standardized values |
| product_cat | STRING | Product category | Accessories | Cannot be null |
| product_sub_cat | STRING | Product subcategory | Bottles and Cages | Cannot be null |
| MAINTENANCE | STRING | Maintenance indicator | No | Allowed: Yes, No |
| prd_start_dt | DATE | Product active start date | 2013-07-01 | Cannot be null |
| prd_end_dt | DATE | Product end date | NULL | Null indicates active product |

---

## Sample Record

```text
product_sk        : 137
prd_id            : 477
prd_key           : WB_H098
product_name      : Water Bottle - 30 oz.
product_cost      : 2.0
product_line      : Standard
product_cat       : Accessories
product_sub_cat   : Bottles and Cages
MAINTENANCE       : No
prd_start_dt      : 2013-07-01
prd_end_dt        : NULL
```

---

## Business Rules

- Product category duplicates removed using:

```python
dropDuplicates(["ID"])
```

- Product keys standardized:

```python
regexp_replace("sls_prd_key","-","_")
```

Example:

| Original | Standardized |
|---|---|
| WB-H098 | WB_H098 |
| BK-R79Y-44 | BK_R79Y_44 |

---

# 3. Fact Table: fact_sales

## Purpose

Stores transactional sales records linked to customers and products.

## Table Grain

One row per sales transaction line item.

## Foreign Keys

- customer_sk
- product_sk

---

## Column Definitions

| Column Name | Data Type | Description | Example Value | Validation Rules |
|---|---|---|---|---|
| sls_ord_num | STRING | Sales order number | SO51259 | Cannot be null |
| sls_order_dt | DATE | Order date | 2013-01-01 | Must be valid date |
| sls_ship_dt | DATE | Shipping date | 2013-01-08 | Must be >= order date |
| sls_due_dt | DATE | Due date | 2013-01-13 | Must be >= ship date |
| customer_sk | BIGINT | FK to dim_customers | 1297080123394 | Must exist in dim_customers |
| product_sk | BIGINT | FK to dim_products | 137 | Must exist in dim_products |
| sls_sales | DOUBLE | Sales amount | 10.0 | Can be negative for returns |
| sls_quantity | INT | Quantity sold | 2 | Must be > 0 |
| sls_price | DOUBLE | Unit price | 2.0 | Null replaced with product cost |
| sls_sales_calc | DOUBLE | Calculated sales amount | 10.0 | Optional validation field |

---

## Sample Record

```text
sls_ord_num      : SO51259
sls_order_dt     : 2013-01-01
sls_ship_dt      : 2013-01-08
sls_due_dt       : 2013-01-13
customer_sk      : 1297080123394
product_sk       : 137
sls_sales        : 10.0
sls_quantity     : 2
sls_price        : 2.0
sls_sales_calc   : 10.0
```

---

## Business Rules

### Missing Price Handling

If sales price is null:

```python
coalesce(col("sls_price"), col("product_cost"))
```

Fallback value:
- product_cost

---

### Return Detection Logic

```python
when(col("sls_price") < 0, 1).otherwise(0)
```

| Price | Return Flag |
|---|---|
| 100 | 0 |
| -100 | 1 |

---

# Star Schema Relationships

```text
                 dim_customers
                 ----------------
                 customer_sk (PK)
                        |
                        |
                        |
fact_sales -------------------------------- dim_products
-----------                                 ----------------
customer_sk (FK)                            product_sk (PK)
product_sk (FK)
```

---

# Data Quality Validations

## Customer Validations

| Validation | Rule |
|---|---|
| Duplicate customers | Removed |
| Null gender | Converted to Unknown |
| Empty names | Converted to Unknown |
| Invalid marital status | Standardized |

---

## Product Validations

| Validation | Rule |
|---|---|
| Duplicate categories | Removed |
| Invalid product keys | Standardized |
| Null product category | Investigated |
| Active product filtering | prd_end_dt IS NULL |

---

## Fact Table Validations

| Validation | Rule |
|---|---|
| Missing product joins | Checked |
| Missing customer joins | Checked |
| Negative prices | Marked as returns |
| Null sales price | Replaced using product cost |
| Invalid dates | Filtered during Silver layer |

---

# ETL Processing Layers

| Layer | Description |
|---|---|
| Bronze | Raw CSV ingestion |
| Silver | Cleansed and standardized source tables |
| Gold | Star schema dimensional model |

---

# Performance Optimizations

| Optimization | Purpose |
|---|---|
| Broadcast Joins | Faster joins with small dimensions |
| Cache/Persist | Avoid recomputation |
| Repartition | Parallel write optimization |
| Column Projection | Reduced memory usage |
| Surrogate Keys | Faster analytical joins |

---

# Storage Format

| Table | Format |
|---|---|
| dim_customers | CSV |
| dim_products | CSV |
| fact_sales | CSV |

---

# Author

Sales Data Analytics Project

PySpark + BigQuery + Medallion Architecture