Medallion Architecture

Create all 3 datasets:

bq mk -d bronze_sales_ds

bq mk -d silver_sales_ds

bq mk -d gold_sales_ds
Result in BigQuery

You will get:

Project
│
├── bronze_sales_ds
├── silver_sales_ds
└── gold_sales_ds
Meaning
Dataset	Purpose
bronze_sales_ds	Raw ingestion data
silver_sales_ds	Cleaned/transformed data
gold_sales_ds	Analytics-ready fact/dim tables
Example Gold Tables

Inside:

gold_sales_ds

you may create:

dim_customer
dim_product
dim_date
fact_sales
Helpful BigQuery Commands
List datasets
bq ls
Show tables
bq ls bronze_sales_ds
Remove dataset
bq rm -r bronze_sales_ds
Best Naming Practice

Professional naming:

bronze_sales_ds
silver_sales_ds
gold_sales_ds

Avoid:

test1
salesdata
newdataset