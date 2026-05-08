


# 3. bronze_load.sh

```bash
#!/bin/bash

# ==========================================
# Create  Dataset
# ==========================================

bq mk -d bronze_sales_ds
bq mk -d silver_sales_ds
bq mk -d gold_sales_ds

# ==========================================
# Load CRM Customers
# ==========================================

bq load \
--source_format=CSV \
--skip_leading_rows=1 \
bronze_sales_ds.crm_customers_raw \
gs://spalika_sales_data/data/cust_info.csv \
"C:\Sreenivas\sales\sales_project\schema\crm_customers_schema.json"

bq head bronze_sales_ds.crm_customers_raw

# ==========================================
# Load CRM Products
# ==========================================

bq load \
--source_format=CSV \
--skip_leading_rows=1 \
bronze_sales_ds.crm_products_raw \
gs://spalika_sales_data/data/prd_info.csv \
"C:\Sreenivas\sales\sales_project\schema\crm_products_schema.json"

bq head bronze_sales_ds.crm_products_raw

# ==========================================
# Load CRM Sales
# ==========================================

bq load \
--source_format=CSV \
--skip_leading_rows=1 \
bronze_sales_ds.crm_sales_raw \
gs://spalika_sales_data/data/sales_details.csv \
"C:\Sreenivas\sales\sales_project\schema\crm_sales_schema.json"

bq head bronze_sales_ds.crm_sales_raw

# ==========================================
# Load ERP Customer Extra
# ==========================================

bq load \
--source_format=CSV \
--skip_leading_rows=1 \
bronze_sales_ds.erp_customer_extra_raw \
gs://spalika_sales_data/data/ERP_CUST_AZ12.csv \
"C:\Sreenivas\sales\sales_project\schema\erp_customer_extra_schema.json"

bq head bronze_sales_ds.erp_customer_extra_raw

# ==========================================
# Load ERP Customer Location
# ==========================================

bq load \
--source_format=CSV \
--skip_leading_rows=1 \
bronze_sales_ds.erp_customer_loc_raw \
gs://spalika_sales_data/data/ERP_LOC_A101.csv \
"C:\Sreenivas\sales\sales_project\schema\erp_customer_loc_schema.json"

bq head bronze_sales_ds.erp_customer_loc_raw

# ==========================================
# Load ERP Product Category
# ==========================================

bq load \
--source_format=CSV \
--skip_leading_rows=1 \
bronze_sales_ds.erp_product_category_raw \
gs://spalika_sales_data/data/ERP_PX_CAT_G1V2.csv \
"C:\Sreenivas\sales\sales_project\schema\erp_product_category_schema.json"

bq head bronze_sales_ds.erp_product_category_raw

# ==========================================
# Verify Bronze Tables
# ==========================================

bq ls bronze_sales_ds
```

---

# Recommended Storage Structure

```text
sales_project/
│
├── scripts/
│   ├── bucket_creation.sh
│   ├── upload_to_bucket.sh
│   └── bronze_load.sh
│
├── schema/
├── data/
├── sql/
└── docs/
```

---

# Execution Commands

## Make Scripts Executable

```bash
chmod +x bucket_creation.sh
chmod +x upload_to_bucket.sh
chmod +x bronze_load.sh
```

---

## Run Scripts

```bash
./bucket_creation.sh
./upload_to_bucket.sh
./bronze_load.sh
```
