# Sales Data Analytics Project Documentation

## Project Overview

The **Sales Data Analytics Project** is a cloud-based data engineering and analytics solution built using:

- Google BigQuery
- Google Cloud Platform (GCP)
- SQL
- Medallion Architecture (Bronze → Silver → Gold)

The project processes CRM and ERP sales datasets to build a modern analytical warehouse for reporting and business intelligence.

---

# Objectives

The main objectives of this project are:

- Build a scalable cloud data warehouse
- Implement Medallion Architecture
- Clean and transform raw business data
- Create analytics-ready datasets
- Prepare data for dashboards and reporting
- Practice real-world data engineering workflows

---

# Architecture

```text
Raw CSV Files
      ↓
Bronze Layer (Raw Ingestion)
      ↓
Silver Layer (Cleaned & Standardized Data)
      ↓
Gold Layer (Business Analytics Layer)
      ↓
Power BI / Looker Studio Dashboards
```

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Google BigQuery | Cloud Data Warehouse |
| SQL | Data Transformation |
| Git | Version Control |
| GitHub | Repository Management |
| CSV Files | Source Data |
| Power BI | Visualization & Reporting |
| Looker Studio | Cloud Dashboards |

---

# Project Structure

```text
sales_project/
│
├── data/
│   ├── crm/
│   └── erp/
│
├── sql/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── notebooks/
│
├── scripts/
│
├── docs/
│
└── README.md
```

---

# Data Sources

## CRM Data

| File | Description |
|---|---|
| cust_info.csv | Customer master information |
| prd_info.csv | Product information |
| sales_details.csv | Sales transaction details |

---

## ERP Data

| File | Description |
|---|---|
| ERP_CUST_AZ12.csv | Additional customer details |
| ERP_LOC_A101.csv | Customer location details |
| ERP_PX_CAT_G1V2.csv | Product category mapping |

---

# Dataset Design

## Bronze Layer

The Bronze Layer stores raw ingested data exactly as received from source systems.

### Characteristics

- No transformations
- Raw historical storage
- Schema preservation
- Source-level auditability

---

## Silver Layer

The Silver Layer contains cleaned and transformed data.

### Implemented Tables

---

## 1. crm_customers

### Purpose
Stores cleaned customer master data.

### Schema

| Column | Data Type |
|---|---|
| cst_id | INTEGER |
| cst_key | STRING |
| cst_firstname | STRING |
| cst_lastname | STRING |
| cst_marital_status | STRING |
| cst_gndr | STRING |
| cst_create_date | DATE |

### Transformations

- Trim whitespace
- Standardize gender values
- Normalize marital status
- Handle null values
- Remove duplicates

---

## 2. crm_products

### Purpose
Stores cleaned product master data.

### Schema

| Column | Data Type |
|---|---|
| prd_id | INTEGER |
| prd_key | STRING |
| prd_nm | STRING |
| prd_cost | FLOAT |
| prd_line | STRING |
| prd_start_dt | DATE |
| prd_end_dt | DATE |

### Transformations

- Product line standardization
- Cost validation
- Date normalization
- Duplicate handling

---

## 3. crm_sales

### Purpose
Stores sales transaction data.

### Schema

| Column | Data Type |
|---|---|
| sls_ord_num | STRING |
| sls_prd_key | STRING |
| sls_cust_id | INTEGER |
| sls_order_dt | DATE |
| sls_ship_dt | DATE |
| sls_due_dt | DATE |
| sls_sales | FLOAT |
| sls_quantity | INTEGER |
| sls_price | FLOAT |

### Transformations

- Date formatting
- Sales validation
- Quantity checks
- Price calculations

---

## 4. erp_customer_extra

### Purpose
Stores additional ERP customer information.

### Schema

| Column | Data Type |
|---|---|
| CID | STRING |
| BDATE | DATE |
| GEN | STRING |

---

## 5. erp_customer_loc

### Purpose
Stores customer geographic details.

### Schema

| Column | Data Type |
|---|---|
| CID | STRING |
| CNTRY | STRING |

---

## 6. erp_product_category

### Purpose
Stores product category mappings.

### Schema

| Column | Data Type |
|---|---|
| ID | STRING |
| CAT | STRING |
| SUBCAT | STRING |
| MAINTENANCE | STRING |

---

# BigQuery Commands Used

## Create Tables

```bash
bq query --use_legacy_sql=false < "path_to_sql_file.sql"
```

---

## List Tables

```bash
bq ls silver_sales_ds
```

---

## View Table Schema

```bash
bq show silver_sales_ds.crm_customers
```

---

# Current Project Status

| Layer | Status |
|---|---|
| Bronze Layer | Completed |
| Silver Table Creation | Completed |
| Silver Data Loading | Pending |
| Gold Layer | Pending |
| Dashboard Development | Pending |

---

# Recommended Next Steps

## 1. Load Data into Silver Tables

Use:

```sql
CREATE OR REPLACE TABLE silver_sales_ds.crm_customers AS
SELECT ...
FROM bronze_sales_ds.crm_customers;
```

---

## 2. Create Gold Layer

### Dimension Tables

- dim_customers
- dim_products
- dim_date

### Fact Tables

- fact_sales

---

## 3. Build Analytics Dashboards

Using:

- Power BI
- Looker Studio

---

# Example Analytics KPIs

| KPI | Description |
|---|---|
| Total Revenue | Overall sales revenue |
| Total Orders | Number of orders |
| Average Order Value | Revenue per order |
| Top Products | Highest-selling products |
| Top Customers | Highest-value customers |
| Sales by Country | Geographic analysis |

---

# Benefits of This Architecture

## Scalability
BigQuery supports petabyte-scale analytics.

## Maintainability
Layered architecture simplifies debugging and transformations.

## Reusability
Silver and Gold datasets can be reused across dashboards and analytics tools.

## Performance
Optimized analytical queries using dimensional modeling.

---

# Learning Outcomes

This project demonstrates practical skills in:

- Cloud Data Engineering
- Data Warehousing
- SQL Transformations
- ETL/ELT Pipelines
- Medallion Architecture
- BigQuery Administration
- Analytics Modeling
- Business Intelligence Integration

---

# Conclusion

The Sales Data Analytics Project provides a complete end-to-end modern data engineering workflow using cloud-native technologies. The implementation follows industry best practices for scalable analytics platforms and prepares data for advanced reporting and business intelligence solutions.

