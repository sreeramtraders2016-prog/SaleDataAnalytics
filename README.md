\# Sales Data Warehouse \& Analytics Project



\## Project Overview



This project demonstrates the design and implementation of a modern Sales Data Warehouse using:



\- PySpark

\- Google BigQuery

\- Google Cloud Storage (GCS)

\- Google Colab

\- Git \& GitHub

\- Jira (SDLC \& Agile tracking)



The solution follows a layered Medallion Architecture:



\- Bronze Layer → Raw ingestion

\- Silver Layer → Cleansed \& transformed data

\- Gold Layer → Business-ready dimensional model



The final solution supports analytics, reporting, and BI use cases using a Star Schema data mart.



\---



\# Project Objectives



The main goals of this project are:



\- Build an end-to-end data engineering pipeline

\- Practice modern ETL/ELT development

\- Implement dimensional modeling

\- Create optimized Spark transformations

\- Build reusable Gold Layer datasets

\- Demonstrate SDLC practices using Jira

\- Maintain version control using GitHub



\---



\# Architecture Overview



\## High-Level Architecture



```text

Source CSV Files

&#x20;      │

&#x20;      ▼

Google Cloud Storage (Bronze)

&#x20;      │

&#x20;      ▼

PySpark Transformations

&#x20;      │

&#x20;      ▼

BigQuery Silver Layer

&#x20;      │

&#x20;      ▼

Gold Layer Dimensions \& Facts

&#x20;      │

&#x20;      ▼

Analytics / Reporting

Source Data Systems



The project uses multiple source systems representing CRM and ERP domains.



CRM Source System



Customer relationship management system providing:



Customer master data

Product master data

Sales transactions

CRM Tables

Table Name	Description

crm\_customers	Customer information

crm\_products	Product information

crm\_sales	Sales transaction data

ERP Source System



Enterprise resource planning system providing:



Product category mappings

Customer demographic data

Customer country/location data

ERP Tables

Table Name	Description

erp\_customer\_extra	Additional customer demographics

erp\_customer\_loc	Customer country/location

erp\_product\_category	Product category hierarchy

Project Folder Structure

sales\_project/

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

Technology Stack

Technology	Purpose

PySpark	Distributed data processing

Google BigQuery	Cloud data warehouse

Google Cloud Storage	Temporary \& raw storage

Google Colab	Development environment

GitHub	Version control

Jira	SDLC \& Agile project tracking

Draw.io	Architecture \& schema diagrams

Data Warehouse Layers

Bronze Layer

Purpose



Stores raw ingested data exactly as received from source systems.



Characteristics

Minimal transformation

Historical preservation

Source-aligned structure

Raw CSV ingestion

Bronze Files

File Name

cust\_info.csv

prd\_info.csv

sales\_details.csv

ERP\_CUST\_AZ12.csv

ERP\_LOC\_A101.csv

ERP\_PX\_CAT\_G1V2.csv

Silver Layer

Purpose



Cleansed and standardized datasets prepared for dimensional modeling.



Transformations

Null handling

Duplicate removal

Standardization

Type casting

Data quality validation

Key normalization

Gold Layer

Purpose



Business-ready analytical layer optimized for reporting and BI.



Gold Tables

Table Name	Type

dim\_customers	Dimension

dim\_products	Dimension

fact\_sales	Fact

Star Schema Design

&#x20;               dim\_customers

&#x20;                    │

&#x20;                    │ customer\_sk

&#x20;                    │

&#x20;                    ▼

&#x20;               fact\_sales

&#x20;                    ▲

&#x20;                    │ product\_sk

&#x20;                    │

&#x20;               dim\_products

Gold Layer Tables

1\. dim\_customers

Description



Customer dimension containing cleaned and enriched customer master data.



Columns

Column Name	Description

customer\_sk	Surrogate key

customer\_id	Business customer ID

customer\_key	CRM customer key

customer\_name	Full customer name

marital\_status	Customer marital status

gender	Standardized gender

birth\_date	Customer birth date

country	Customer country

customer\_create\_date	CRM creation date

2\. dim\_products

Description



Product dimension containing product attributes and category hierarchy.



Columns

Column Name	Description

product\_sk	Surrogate key

prd\_id	Product ID

prd\_key	Product business key

product\_name	Product name

product\_cost	Product cost

product\_line	Product line

product\_cat	Product category

product\_sub\_cat	Product subcategory

maintenance	Maintenance indicator

prd\_start\_dt	Product start date

prd\_end\_dt	Product end date

3\. fact\_sales

Description



Fact table containing transactional sales measures.



Columns

Column Name	Description

sls\_ord\_num	Sales order number

sls\_order\_dt	Order date

sls\_ship\_dt	Shipping date

sls\_due\_dt	Due date

customer\_sk	Customer surrogate key

product\_sk	Product surrogate key

sls\_sales	Sales amount

sls\_quantity	Quantity sold

sls\_price	Unit price

sls\_sales\_calc	Calculated sales value

Data Quality \& Validation Rules

Customer Validations

Validation	Rule

Duplicate customers	Removed using dropDuplicates

Gender standardization	M/F converted to Male/Female

Null names	Replaced with Unknown

Country cleanup	Standardized values

Product Validations

Validation	Rule

Duplicate categories	Removed

Product key normalization	Hyphen replaced with underscore

Null category handling	Managed during joins

Sales Validations

Validation	Rule

Product key mismatch	Standardized using regexp\_replace

Null prices	Replaced using product cost

Return detection	Negative price flagged

Foreign key joins	Validated against dimensions

Performance Optimization Techniques



The project includes several Spark optimization strategies.



Implemented Optimizations

Technique	Purpose

Broadcast joins	Faster small-table joins

Repartitioning	Improved parallelism

Caching	Reduce recomputation

Column pruning	Reduced memory usage

Deduplication	Improved data quality

Predicate filtering	Faster processing

PySpark Features Used

Transformations

select()

withColumn()

filter()

dropDuplicates()

join()

alias()

repartition()

Functions

when()

col()

upper()

trim()

concat\_ws()

regexp\_replace()

coalesce()

monotonically\_increasing\_id()

Window Functions

row\_number()

Window.partitionBy()

SDLC \& Project Management

Jira Usage



Jira was used to manage the Software Development Life Cycle (SDLC).



Activities Managed in Jira

Requirement tracking

Task management

Sprint planning

ETL pipeline development tracking

Bug tracking

Documentation tracking

Git \& GitHub Workflow

Git Commands Used

git status

git add .

git commit -m "Implemented bronze and gold layer sales warehouse pipelines"

git push origin main

Repository Features

Version control

Commit history

Documentation tracking

Notebook management

Collaborative workflow support

Sample Data Flow

CSV Files

&#x20;  ↓

Bronze Layer

&#x20;  ↓

Silver Cleansing

&#x20;  ↓

Gold Dimensions

&#x20;  ↓

Fact Table Creation

&#x20;  ↓

Star Schema

&#x20;  ↓

Analytics

Example Business Use Cases



The warehouse can support:



Sales trend analysis

Product performance reporting

Customer segmentation

Country-wise sales analytics

Return analysis

Revenue dashboards

Future Enhancements



Potential improvements include:



Incremental loading

Slowly Changing Dimensions (SCD)

Airflow orchestration

BI dashboard integration

Data quality monitoring

CI/CD pipelines

Automated testing

Conclusion



This project demonstrates:



End-to-end data engineering workflows

Cloud-native analytics architecture

Dimensional modeling

PySpark optimization techniques

Real-world ETL design

SDLC best practices

Production-style documentation



The final solution provides a scalable and analytics-ready Sales Data Warehouse architectur

