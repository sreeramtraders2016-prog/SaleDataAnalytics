# Sales Data Warehouse & Analytics Project

---

# Table of Contents

1. Project Overview
2. Project Objectives
3. Architecture Overview
4. Source Data Systems
5. Project Folder Structure
6. Technology Stack
7. Data Warehouse Layers
8. Star Schema Design
9. Gold Layer Tables
10. Data Dictionary
11. Data Quality & Validation Rules
12. Performance Optimization Techniques
13. PySpark Features Used
14. SDLC & Project Management
15. Git & GitHub Workflow
16. Sample Data Flow
17. Example Business Use Cases
18. Future Enhancements
19. Conclusion

---

# 1. Project Overview

This project demonstrates the design and implementation of a modern Sales Data Warehouse using:

- PySpark
- Google BigQuery
- Google Cloud Storage (GCS)
- Google Colab
- Git & GitHub
- Jira (SDLC & Agile tracking)

The solution follows a layered Medallion Architecture:

- Bronze Layer → Raw ingestion
- Silver Layer → Cleansed & transformed data
- Gold Layer → Business-ready dimensional model

The final solution supports analytics, reporting, and BI use cases using a Star Schema data mart.

---

# 2. Project Objectives

The main goals of this project are:

- Build an end-to-end data engineering pipeline
- Practice modern ETL/ELT development
- Implement dimensional modeling
- Create optimized Spark transformations
- Build reusable Gold Layer datasets
- Demonstrate SDLC practices using Jira
- Maintain version control using GitHub

---

# 3. Architecture Overview

## High-Level Architecture

```text
Source CSV Files
       │
       ▼
Google Cloud Storage (Bronze)
       │
       ▼
PySpark Transformations
       │
       ▼
BigQuery Silver Layer
       │
       ▼
Gold Layer Dimensions & Facts
       │
       ▼
Analytics / Reporting
```

---

# 4. Source Data Systems

The project uses multiple source systems representing CRM and ERP domains.

---

## CRM Source System

Customer relationship management system providing:

- Customer master data
- Product master data
- Sales transactions

### CRM Tables

| Table Name | Description |
|---|---|
| crm_customers | Customer information |
| crm_products | Product information |
| crm_sales | Sales transaction data |

---

## ERP Source System

Enterprise resource planning system providing:

- Product category mappings
- Customer demographic data
- Customer country/location data

### ERP Tables

| Table Name | Description |
|---|---|
| erp_customer_extra | Additional customer demographics |
| erp_customer_loc | Customer country/location |
| erp_product_category | Product category hierarchy |

---

# 5. Project Folder Structure

```text
sales_project/
│
├── data/
│   ├── bronze/
│   └── gold/
│
├── notebooks/
│   ├── Bronze/
│   ├── Silver/
│   └── Gold/
│
├── doc/
│
└── README.md
```

---

# 6. Technology Stack

| Technology | Purpose |
|---|---|
| PySpark | Distributed data processing |
| Google BigQuery | Cloud data warehouse |
| Google Cloud Storage | Temporary & raw storage |
| Google Colab | Development environment |
| GitHub | Version control |
| Jira | SDLC & Agile project tracking |
| Draw.io | Architecture & schema diagrams |

---

# 7. Data Warehouse Layers

# Bronze Layer

## Purpose

Stores raw ingested data exactly as received from source systems.

## Characteristics

- Minimal transformation
- Historical preservation
- Source-aligned structure
- Raw CSV ingestion

## Bronze Files

| File Name |
|---|
| cust_info.csv |
| prd_info.csv |
| sales_details.csv |
| ERP_CUST_AZ12.csv |
| ERP_LOC_A101.csv |
| ERP_PX_CAT_G1V2.csv |

---

# Silver Layer

## Purpose

Cleansed and standardized datasets prepared for dimensional modeling.

## Transformations

- Null handling
- Duplicate removal
- Standardization
- Type casting
- Data quality validation
- Key normalization

---

# Gold Layer

## Purpose

Business-ready analytical layer optimized for reporting and BI.

## Gold Tables

| Table Name | Type |
|---|---|
| dim_customers | Dimension |
| dim_products | Dimension |
| fact_sales | Fact |

---

# 8. Star Schema Design

```text
                dim_customers
                     │
                     │ customer_sk
                     │
                     ▼
                fact_sales
                     ▲
                     │ product_sk
                     │
                dim_products
```

---

# 9. Gold Layer Tables

# 1. dim_customers

## Description

Customer dimension containing cleaned and enriched customer master data.

## Columns

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
| customer_create_date | CRM creation date |

---

# 2. dim_products

## Description

Product dimension containing product attributes and category hierarchy.

## Columns

| Column Name | Description |
|---|---|
| product_sk | Surrogate key |
| prd_id | Product ID |
| prd_key | Product business key |
| product_name | Product name |
| product_cost | Product cost |
| product_line | Product line |
| product_cat | Product category |
| product_sub_cat | Product subcategory |
| maintenance | Maintenance indicator |
| prd_start_dt | Product start date |
| prd_end_dt | Product end date |

---

# 3. fact_sales

## Description

Fact table containing transactional sales measures.

## Columns

| Column Name | Description |
|---|---|
| sls_ord_num | Sales order number |
| sls_order_dt | Order date |
| sls_ship_dt | Shipping date |
| sls_due_dt | Due date |
| customer_sk | Customer surrogate key |
| product_sk | Product surrogate key |
| sls_sales | Sales amount |
| sls_quantity | Quantity sold |
| sls_price | Unit price |
| sls_sales_calc | Calculated sales value |

---

# 10. Data Dictionary

## dim_customers

| Column | Data Type | Example Value | Validation |
|---|---|---|---|
| customer_sk | BIGINT | 1001 | Unique surrogate key |
| customer_id | INT | 11000 | Must not be null |
| customer_key | STRING | AW00011000 | CRM business key |
| customer_name | STRING | John Smith | Nulls replaced with Unknown |
| marital_status | STRING | Married | Standardized values |
| gender | STRING | Male | M/F mapped to Male/Female |
| birth_date | DATE | 1985-04-12 | Valid date only |
| country | STRING | United States | Standardized country |
| customer_create_date | DATE | 2025-10-07 | Source create date |

---

## dim_products

| Column | Data Type | Example Value | Validation |
|---|---|---|---|
| product_sk | BIGINT | 5001 | Unique surrogate key |
| prd_id | INT | 501 | Must not be null |
| prd_key | STRING | BK_R79Y_44 | Hyphen standardized |
| product_name | STRING | Road Bike | Product description |
| product_cost | DOUBLE | 1200.50 | Positive numeric value |
| product_line | STRING | Road | Standardized category |
| product_cat | STRING | Bikes | Product hierarchy |
| product_sub_cat | STRING | Road Bikes | Product hierarchy |
| maintenance | STRING | Yes | Yes/No values |
| prd_start_dt | DATE | 2013-07-01 | Effective date |
| prd_end_dt | DATE | NULL | Nullable active product |

---

## fact_sales

| Column | Data Type | Example Value | Validation |
|---|---|---|---|
| sls_ord_num | STRING | SO51259 | Unique order number |
| sls_order_dt | DATE | 2013-01-01 | Valid order date |
| sls_ship_dt | DATE | 2013-01-08 | Must be >= order date |
| sls_due_dt | DATE | 2013-01-13 | Must be >= ship date |
| customer_sk | BIGINT | 1001 | FK to dim_customers |
| product_sk | BIGINT | 5001 | FK to dim_products |
| sls_sales | DOUBLE | 1701.00 | Positive sales amount |
| sls_quantity | INT | 1 | Positive quantity |
| sls_price | DOUBLE | 1701.00 | Nulls replaced using product cost |
| sls_sales_calc | DOUBLE | 1701.00 | Calculated sales value |

---

# 11. Data Quality & Validation Rules

## Customer Validations

| Validation | Rule |
|---|---|
| Duplicate customers | Removed using dropDuplicates |
| Gender standardization | M/F converted to Male/Female |
| Null names | Replaced with Unknown |
| Country cleanup | Standardized values |

---

## Product Validations

| Validation | Rule |
|---|---|
| Duplicate categories | Removed |
| Product key normalization | Hyphen replaced with underscore |
| Null category handling | Managed during joins |

---

## Sales Validations

| Validation | Rule |
|---|---|
| Product key mismatch | Standardized using regexp_replace |
| Null prices | Replaced using product cost |
| Return detection | Negative price flagged |
| Foreign key joins | Validated against dimensions |

---

# 12. Performance Optimization Techniques

The project includes several Spark optimization strategies.

## Implemented Optimizations

| Technique | Purpose |
|---|---|
| Broadcast joins | Faster small-table joins |
| Repartitioning | Improved parallelism |
| Caching | Reduce recomputation |
| Column pruning | Reduced memory usage |
| Deduplication | Improved data quality |
| Predicate filtering | Faster processing |

---

# 13. PySpark Features Used

## Transformations

- select()
- withColumn()
- filter()
- dropDuplicates()
- join()
- alias()
- repartition()

## Functions

- when()
- col()
- upper()
- trim()
- concat_ws()
- regexp_replace()
- coalesce()
- monotonically_increasing_id()

## Window Functions

- row_number()
- Window.partitionBy()

---

# 14. SDLC & Project Management

## Jira Usage

Jira was used to manage the Software Development Life Cycle (SDLC).

### Activities Managed in Jira

- Requirement tracking
- Task management
- Sprint planning
- ETL pipeline development tracking
- Bug tracking
- Documentation tracking

---

# 15. Git & GitHub Workflow

## Git Commands Used

```bash
git status
git add .
git commit -m "Implemented bronze and gold layer sales warehouse pipelines"
git push origin main
```

## Repository Features

- Version control
- Commit history
- Documentation tracking
- Notebook management
- Collaborative workflow support

---

# 16. Sample Data Flow

```text
CSV Files
   ↓
Bronze Layer
   ↓
Silver Cleansing
   ↓
Gold Dimensions
   ↓
Fact Table Creation
   ↓
Star Schema
   ↓
Analytics
```

---

# 17. Example Business Use Cases

The warehouse can support:

- Sales trend analysis
- Product performance reporting
- Customer segmentation
- Country-wise sales analytics
- Return analysis
- Revenue dashboards

---

# 18. Future Enhancements

Potential improvements include:

- Incremental loading
- Slowly Changing Dimensions (SCD)
- Airflow orchestration
- BI dashboard integration
- Data quality monitoring
- CI/CD pipelines
- Automated testing

---

# 19. Conclusion

This project demonstrates:

- End-to-end data engineering workflows
- Cloud-native analytics architecture
- Dimensional modeling
- PySpark optimization techniques
- Real-world ETL design
- SDLC best practices
- Production-style documentation

The final solution provides a scalable and analytics-ready Sales Data Warehouse architecture.

