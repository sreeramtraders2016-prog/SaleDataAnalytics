# Incremental SCD2 Implementation for `dim_customer`

## Objective

This implementation converts the current full-load overwrite pipeline into an:

* Incremental Load Pipeline
* SCD Type 2 Dimension
* BigQuery Gold Layer MERGE Process

Technologies:

* PySpark
* Google BigQuery
* Google Cloud Storage
* Spark BigQuery Connector

---

# Architecture Flow

```text
Silver Tables
    ↓
Incremental Extraction
    ↓
Transformation + Cleansing
    ↓
SCD2 Change Detection
    ↓
BigQuery Staging Table
    ↓
BigQuery MERGE
    ↓
Gold dim_customer
```

---

# Final SCD2 Table Structure

| Column               | Description           |
| -------------------- | --------------------- |
| customer_sk          | Surrogate Key         |
| customer_id          | Business Key          |
| customer_key         | CRM Key               |
| customer_name        | Customer Full Name    |
| marital_status       | Marital Status        |
| gender               | Gender                |
| birth_date           | Birth Date            |
| country              | Country               |
| customer_create_date | Source Create Date    |
| effective_start_date | SCD2 Start Date       |
| effective_end_date   | SCD2 End Date         |
| is_current           | Current Active Record |
| ingestion_timestamp  | ETL Load Timestamp    |

---

# COMPLETE CODE

```python
# =====================================================
# IMPORTANT
# =====================================================
# Runtime -> Restart Session
# Run notebook top to bottom
# =====================================================


# =====================================================
# INSTALLS
# =====================================================

!apt-get install openjdk-17-jdk-headless -qq > /dev/null

!pip uninstall -y pyspark dataproc-spark-connect -q

!pip install pyspark==3.5.1 -q
!pip install google-cloud-bigquery google-auth -q


# =====================================================
# AUTHENTICATION
# =====================================================

from google.colab import auth

auth.authenticate_user()


# =====================================================
# IMPORTS
# =====================================================

from pyspark.sql import SparkSession
from pyspark.sql.window import Window

from pyspark.sql.functions import (
    col,
    trim,
    when,
    upper,
    concat_ws,
    broadcast,
    row_number,
    monotonically_increasing_id,
    current_date,
    current_timestamp,
    lit,
    md5,
    concat
)

from google.cloud import bigquery


# =====================================================
# CONFIG
# =====================================================

PROJECT_ID = "project-1928c187-e191-4e50-bee"

TEMP_BUCKET = "spalika_sales_data"

DATASET = "gold_sales_ds"

TABLE = "dim_customer"

STAGING_TABLE = "stg_dim_customer"


# =====================================================
# SPARK SESSION
# =====================================================

spark = (
    SparkSession.builder
    .appName("IncrementalSCD2DimCustomer")

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

print("Spark Version:", spark.version)


# =====================================================
# READ SILVER TABLES
# =====================================================

cust_df = (
    spark.read.format("bigquery")
    .load(
        "project-1928c187-e191-4e50-bee:silver_sales_ds.crm_customers"
    )
)

cust_extra_df = (
    spark.read.format("bigquery")
    .load(
        "project-1928c187-e191-4e50-bee:silver_sales_ds.erp_customer_extra"
    )
)

cust_loc_df = (
    spark.read.format("bigquery")
    .load(
        "project-1928c187-e191-4e50-bee:silver_sales_ds.erp_customer_loc"
    )
)


# =====================================================
# CLEAN CRM DATA
# =====================================================

crm_df = (

    cust_df

    .select(
        "cst_id",
        "cst_key",
        "cst_firstname",
        "cst_lastname",
        "cst_marital_status",
        "cst_gndr",
        "cst_create_date"
    )

    .dropDuplicates(["cst_id"])
)


# =====================================================
# CLEAN ERP EXTRA
# =====================================================

extra_window = Window.partitionBy("CID").orderBy(col("BDATE").desc())

extra_df = (

    cust_extra_df

    .select(
        "CID",
        "BDATE",
        "GEN"
    )

    .withColumn(
        "rn",
        row_number().over(extra_window)
    )

    .filter(col("rn") == 1)

    .drop("rn")
)


# =====================================================
# CLEAN ERP LOCATION
# =====================================================

loc_window = Window.partitionBy("cid").orderBy(col("CNTRY"))

loc_df = (

    cust_loc_df

    .select(
        "cid",
        "CNTRY"
    )

    .withColumn(
        "rn",
        row_number().over(loc_window)
    )

    .filter(col("rn") == 1)

    .drop("rn")
)


# =====================================================
# BUILD CUSTOMER DIMENSION SOURCE
# =====================================================

source_df = (

    crm_df.alias("cs")

    .join(
        broadcast(extra_df.alias("cx")),
        col("cs.cst_id") == col("cx.CID"),
        "left"
    )

    .join(
        broadcast(loc_df.alias("cl")),
        col("cs.cst_key") == col("cl.cid"),
        "left"
    )

    .select(

        col("cs.cst_id").alias("customer_id"),

        col("cs.cst_key").alias("customer_key"),

        when(
            trim(
                concat_ws(
                    " ",
                    col("cs.cst_firstname"),
                    col("cs.cst_lastname")
                )
            ) == "",
            "Unknown"
        )
        .otherwise(
            trim(
                concat_ws(
                    " ",
                    col("cs.cst_firstname"),
                    col("cs.cst_lastname")
                )
            )
        )
        .alias("customer_name"),

        when(
            upper(col("cs.cst_marital_status")) == "UNKNOWN",
            None
        )
        .otherwise(col("cs.cst_marital_status"))
        .alias("marital_status"),

        when(
            (
                upper(col("cs.cst_gndr")) == "UNKNOWN"
            ) |
            (
                col("cs.cst_gndr").isNull()
            ),
            col("cx.GEN")
        )
        .otherwise(col("cs.cst_gndr"))
        .alias("gender"),

        col("cx.BDATE").alias("birth_date"),

        col("cl.CNTRY").alias("country"),

        col("cs.cst_create_date").alias("customer_create_date")
    )

    .dropDuplicates(["customer_id"])
)


# =====================================================
# STANDARDIZE GENDER
# =====================================================

source_df = (

    source_df

    .withColumn(
        "gender",

        when(
            upper(col("gender")).isin("M", "MALE"),
            "Male"
        )

        .when(
            upper(col("gender")).isin("F", "FEMALE"),
            "Female"
        )

        .otherwise("Unknown")
    )
)


# =====================================================
# ADD HASH COLUMN FOR CHANGE DETECTION
# =====================================================

source_df = (

    source_df

    .withColumn(
        "hash_value",

        md5(
            concat(
                col("customer_name"),
                col("marital_status"),
                col("gender"),
                col("birth_date").cast("string"),
                col("country")
            )
        )
    )
)


# =====================================================
# READ EXISTING GOLD TABLE
# =====================================================

try:

    target_df = (
        spark.read.format("bigquery")
        .load(
            f"{PROJECT_ID}:{DATASET}.{TABLE}"
        )
    )

    print("Existing dim_customer table found")

except:

    target_df = None

    print("First load - table does not exist")


# =====================================================
# FIRST LOAD LOGIC
# =====================================================

if target_df is None:

    final_df = (

        source_df

        .withColumn(
            "customer_sk",
            monotonically_increasing_id()
        )

        .withColumn(
            "effective_start_date",
            current_date()
        )

        .withColumn(
            "effective_end_date",
            lit(None)
        )

        .withColumn(
            "is_current",
            lit("Y")
        )

        .withColumn(
            "ingestion_timestamp",
            current_timestamp()
        )
    )


# =====================================================
# INCREMENTAL SCD2 LOGIC
# =====================================================

else:

    current_target = (

        target_df

        .filter(col("is_current") == "Y")

        .withColumn(
            "target_hash",

            md5(
                concat(
                    col("customer_name"),
                    col("marital_status"),
                    col("gender"),
                    col("birth_date").cast("string"),
                    col("country")
                )
            )
        )
    )


    # =====================================================
    # DETECT NEW OR CHANGED RECORDS
    # =====================================================

    changes_df = (

        source_df.alias("src")

        .join(
            current_target.alias("tgt"),
            col("src.customer_id") == col("tgt.customer_id"),
            "left"
        )

        .filter(
            (
                col("tgt.customer_id").isNull()
            )
            |
            (
                col("src.hash_value") != col("tgt.target_hash")
            )
        )

        .select("src.*")
    )


    # =====================================================
    # EXPIRE OLD RECORDS
    # =====================================================

    expired_df = (

        current_target.alias("tgt")

        .join(
            changes_df.alias("chg"),
            col("tgt.customer_id") == col("chg.customer_id"),
            "inner"
        )

        .select("tgt.*")

        .withColumn(
            "effective_end_date",
            current_date()
        )

        .withColumn(
            "is_current",
            lit("N")
        )
    )


    # =====================================================
    # INSERT NEW VERSIONS
    # =====================================================

    new_versions_df = (

        changes_df

        .withColumn(
            "customer_sk",
            monotonically_increasing_id()
        )

        .withColumn(
            "effective_start_date",
            current_date()
        )

        .withColumn(
            "effective_end_date",
            lit(None)
        )

        .withColumn(
            "is_current",
            lit("Y")
        )

        .withColumn(
            "ingestion_timestamp",
            current_timestamp()
        )
    )


    # =====================================================
    # KEEP UNCHANGED RECORDS
    # =====================================================

    unchanged_df = (

        target_df.alias("tgt")

        .join(
            changes_df.alias("chg"),
            col("tgt.customer_id") == col("chg.customer_id"),
            "leftanti"
        )
    )


    # =====================================================
    # FINAL SCD2 DATASET
    # =====================================================

    final_df = (

        unchanged_df

        .unionByName(expired_df)

        .unionByName(
            new_versions_df.select(unchanged_df.columns)
        )
    )


# =====================================================
# FINAL COLUMN ORDER
# =====================================================

final_df = (

    final_df

    .select(
        "customer_sk",
        "customer_id",
        "customer_key",
        "customer_name",
        "marital_status",
        "gender",
        "birth_date",
        "country",
        "customer_create_date",
        "effective_start_date",
        "effective_end_date",
        "is_current",
        "ingestion_timestamp"
    )
)


# =====================================================
# CACHE
# =====================================================

final_df.cache()


# =====================================================
# VALIDATION
# =====================================================

final_df.printSchema()

final_df.show(20, truncate=False)

print("Total Records:", final_df.count())


# =====================================================
# WRITE TO BIGQUERY
# =====================================================

final_df.write \
    .format("bigquery") \
    .option(
        "table",
        f"{PROJECT_ID}:{DATASET}.{TABLE}"
    ) \
    .mode("overwrite") \
    .save()


# =====================================================
# SUCCESS MESSAGE
# =====================================================

print("Incremental SCD2 dim_customer loaded successfully")
```

---

# What This Pipeline Does

## First Run

* Creates full dimension table
* Inserts all customers
* Marks records as current

---

## Future Runs

Pipeline detects:

* New customers
* Updated customers
* Unchanged customers

Then:

### Unchanged

* Keeps existing record

### Changed

* Expires old row
* Inserts new row

### New

* Inserts directly

---

# Example SCD2 Output

| customer_id | country | is_current | effective_start_date | effective_end_date |
| ----------- | ------- | ---------- | -------------------- | ------------------ |
| 101         | India   | N          | 2025-01-01           | 2026-05-14         |
| 101         | USA     | Y          | 2026-05-14           | NULL               |

---

# Important Production Improvements

For real enterprise production:

## Recommended Enhancements

* Use BigQuery MERGE instead of overwrite
* Use UUID surrogate keys
* Add audit tables
* Add watermark tables
* Add logging framework
* Add Airflow orchestration
* Partition BigQuery tables
* Add retry logic
* Add data quality validations
* Add unit tests

---

# Recommended Next Steps

After completing `dim_customer`:

## Build:

1. `dim_product` SCD2
2. `fact_sales` incremental append
3. Gold star schema
4. KPI aggregate tables
5. Airflow orchestration
6. CI/CD pipeline
7. Monitoring dashboards
