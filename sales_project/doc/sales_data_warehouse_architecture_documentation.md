# Sales Data Analytics Platform Documentation

## Overview

This document describes the architecture, data integration process, and layered data warehouse design used in the Sales Data Analytics project.

The platform integrates CRM and ERP systems into a modern analytical data warehouse using the Medallion Architecture pattern:

- Bronze Layer → Raw ingestion
- Silver Layer → Cleansed and standardized data
- Gold Layer → Business-ready analytical models

The solution supports scalable analytics, reporting, and business intelligence workloads.

---

# 1. High-Level Architecture

## Architecture Summary

The architecture follows a layered approach:

1. Source Systems
   - CRM System
   - ERP System

2. Data Ingestion Layer (Bronze)
   - Raw batch ingestion
   - Minimal transformations
   - Historical preservation

3. Data Processing Layer (Silver)
   - Data cleansing
   - Standardization
   - Enrichment
   - Integration

4. Business Layer (Gold)
   - Star schema modeling
   - Business aggregations
   - KPI-ready datasets

5. Consumer Layer
   - BI dashboards
   - Reporting tools
   - Ad-hoc analytics
   - Data science workloads

---

## Refined Architecture Design

![High-Level Data Warehouse Architecture](sandbox:/mnt/data/5bf66944-bb57-4b22-9e36-f51e8ca485f2.png)

### Architecture Diagram

```text
+---------------------------------------------------------------+
|                     DATA WAREHOUSE PLATFORM                   |
+---------------------------------------------------------------+

+-------------+       +-------------+       +-------------+
|   SOURCES   | ----> |   BRONZE    | ----> |   SILVER    |
+-------------+       +-------------+       +-------------+
| CRM System  |       | Raw Data    |       | Cleansed    |
| ERP System  |       | Batch Load  |       | Standardized|
| CSV Files   |       | Append/Merge|       | Enriched    |
+-------------+       +-------------+       +-------------+
                                                   |
                                                   v
                                           +-------------+
                                           |    GOLD     |
                                           +-------------+
                                           | Star Schema |
                                           | Aggregation |
                                           | Business KPIs|
                                           +-------------+
                                                   |
                                                   v
                                           +-------------+
                                           | CONSUMERS   |
                                           +-------------+
                                           | Power BI    |
                                           | Dashboards  |
                                           | Analytics   |
                                           +-------------+
```

---

# 2. Medallion Architecture Layers

## 2.1 Bronze Layer

### Purpose
The Bronze layer stores raw ingested data exactly as received from source systems.

### Characteristics

| Feature | Description |
|---|---|
| Data State | Raw / Unprocessed |
| Load Type | Full Load / Incremental |
| Transformations | Minimal |
| Data Quality Rules | Very Limited |
| Storage Pattern | Append / Merge |
| Schema | Source-Oriented |

### Responsibilities

- Ingest CRM and ERP source files
- Preserve historical source data
- Support replay and recovery
- Maintain auditability

### Typical Operations

- File ingestion
- Metadata capture
- Load timestamp generation
- Basic null handling
- Deduplication (optional)

### Example Tables

| Table Name | Description |
|---|---|
| bronze.crm_sales_details | Raw sales transactions |
| bronze.crm_cust_info | Raw customer data |
| bronze.crm_prd_info | Raw product data |
| bronze.erp_cust_loc | Raw customer location data |
| bronze.erp_cust | Raw customer demographic data |
| bronze.erp_prd_cat | Raw product category data |

---

## 2.2 Silver Layer

### Purpose
The Silver layer stores cleaned, standardized, and integrated datasets.

### Characteristics

| Feature | Description |
|---|---|
| Data State | Cleansed and Validated |
| Transformations | Medium Complexity |
| Data Quality | High |
| Schema | Integrated |
| Processing | Business-neutral |

### Responsibilities

- Data cleansing
- Data standardization
- Data enrichment
- Integration of CRM and ERP data
- Data validation

### Common Transformations

#### Data Cleaning

- Remove duplicates
- Handle null values
- Fix invalid records
- Correct date formats

#### Standardization

- Standardize gender values
- Normalize product keys
- Standardize country/location names
- Format customer identifiers

#### Enrichment

- Derived columns
- Age calculations
- Product hierarchy mapping
- Customer segmentation

### Typical Processing Logic

```sql
Example:
- Standardize product keys
- Convert dates
- Generate derived metrics
- Validate customer IDs
```

### Example Tables

| Table Name | Description |
|---|---|
| silver.crm_sales_details | Cleaned sales transactions |
| silver.crm_cust_info | Standardized customer master |
| silver.crm_prd_info | Enriched product master |
| silver.erp_cust_loc | Standardized customer locations |
| silver.erp_cust | Validated customer demographics |
| silver.erp_prd_cat | Product category mappings |

---

## 2.3 Gold Layer

### Purpose
The Gold layer provides business-ready analytical datasets optimized for reporting and BI.

### Characteristics

| Feature | Description |
|---|---|
| Data State | Business Ready |
| Model Type | Star Schema |
| Consumers | BI / Analytics |
| Aggregation | High |
| Transformations | Business Logic |

### Responsibilities

- Build dimensional models
- Create fact tables
- Create aggregated datasets
- Apply business rules
- Support KPI reporting

### Gold Layer Components

#### Dimension Tables

| Table | Description |
|---|---|
| dim_customer | Customer master dimension |
| dim_product | Product dimension |
| dim_date | Calendar/date dimension |

#### Fact Tables

| Table | Description |
|---|---|
| fact_sales | Sales transactional fact table |

#### Aggregation Tables

| Table | Description |
|---|---|
| agg_sales_monthly | Monthly sales summary |
| agg_product_performance | Product performance metrics |
| agg_customer_sales | Customer-level sales metrics |

---

# 3. Data Integration Design

## Objective
The integration process combines CRM operational data with ERP master/reference data to create a unified analytical model.

---

## Source Systems

### CRM System

Provides:

- Sales transactions
- Customer master data
- Product information

### ERP System

Provides:

- Customer locations
- Customer demographics
- Product category mappings

---

# 4. Refined Data Integration Flow

![CRM and ERP Data Integration Architecture](sandbox:/mnt/data/81b96f4d-a479-4ac6-84d0-c8f0a7cc5a90.png)

## Integration Architecture Diagram

```text
CRM SOURCES
------------
crm_sales_details
    |-- sls_cust_id
    |-- sls_prd_key

crm_cust_info
    |-- cust_id

crm_prd_info
    |-- prd_key

ERP SOURCES
------------
erp_cust_loc
    |-- cid

erp_cust
    |-- cid

erp_prd_cat
    |-- id

INTEGRATION LOGIC
-----------------
1. crm_sales_details joins crm_cust_info using customer ID
2. crm_sales_details joins crm_prd_info using product key
3. crm_cust_info joins ERP customer tables using customer ID
4. crm_prd_info joins ERP product category using product category ID

OUTPUT
------
Unified analytical model for Gold layer
```

---

# 5. Integration Mapping

## Customer Integration

| CRM Table | ERP Table | Join Key | Purpose |
|---|---|---|---|
| crm_cust_info | erp_cust_loc | cust_id = cid | Customer location enrichment |
| crm_cust_info | erp_cust | cust_id = cid | Customer demographic enrichment |

### Output Attributes

- Customer Name
- Gender
- Birth Date
- Country
- City
- Customer Type

---

## Product Integration

| CRM Table | ERP Table | Join Key | Purpose |
|---|---|---|---|
| crm_prd_info | erp_prd_cat | product category id | Product categorization |

### Output Attributes

- Product Name
- Product Category
- Product Subcategory
- Product Maintenance Flag

---

## Sales Integration

| Source Table | Description |
|---|---|
| crm_sales_details | Transactional sales data |

### Measures

- Sales Amount
- Quantity Sold
- Unit Price
- Order Date
- Shipping Date

---

# 6. Data Flow Lifecycle

## Step 1 — Source Extraction

Data is extracted from:

- CRM CSV files
- ERP CSV files
- External operational systems

---

## Step 2 — Bronze Ingestion

Raw data is loaded into Bronze tables.

### Key Activities

- Batch ingestion
- File validation
- Metadata generation
- Raw archival

---

## Step 3 — Silver Transformation

Data quality and standardization processes are applied.

### Key Activities

- Null handling
- Deduplication
- Standardization
- Type conversion
- Business-neutral transformations

---

## Step 4 — Gold Modeling

Business logic and dimensional modeling are implemented.

### Key Activities

- Fact table creation
- Dimension creation
- KPI generation
- Aggregation logic

---

## Step 5 — Consumption

Business users consume curated datasets.

### Consumption Tools

- Power BI
- Tableau
- SQL Analytics
- Machine Learning Models

---

# 7. Recommended Naming Standards

## Layer Prefixes

| Layer | Prefix Example |
|---|---|
| Bronze | bronze.* |
| Silver | silver.* |
| Gold | gold.* |

---

## Table Naming Convention

| Type | Example |
|---|---|
| Fact Table | fact_sales |
| Dimension Table | dim_customer |
| Aggregate Table | agg_monthly_sales |

---

## Column Naming Convention

| Convention | Example |
|---|---|
| Primary Key | customer_key |
| Foreign Key | customer_id |
| Date Column | order_date |
| Timestamp | ingestion_dt |

---

# 8. Data Quality Rules

## Customer Data Rules

- Customer ID must not be null
- Birth date must be valid
- Customer age should be between valid ranges

## Product Data Rules

- Product key must be unique
- Product category must exist

## Sales Data Rules

- Sales amount must be positive
- Quantity must be greater than zero
- Order date cannot exceed current date

---

# 9. Recommended Technology Stack

| Layer | Technology |
|---|---|
| Processing | PySpark |
| Storage | BigQuery / Delta Lake |
| Notebook | Google Colab |
| Orchestration | Airflow (Future) |
| BI | Power BI |
| Language | Python / SQL |

---

# 10. Future Enhancements

## Recommended Improvements

### Incremental Processing

- CDC support
- Watermarking
- Incremental merge logic

### Data Governance

- Data catalog
- Lineage tracking
- Schema evolution

### Performance Optimization

- Partitioning
- Clustering
- Caching
- Materialized views

### Security

- Role-based access control
- Column-level security
- Data masking

---

# 11. Conclusion

This architecture provides:

- Scalable data integration
- Clean separation of responsibilities
- Improved data quality
- Business-ready analytics
- Maintainable transformation pipelines

The Medallion Architecture ensures that raw operational data evolves into trusted analytical datasets suitable for enterprise reporting and decision-making.

