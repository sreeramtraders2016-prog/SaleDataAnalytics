@echo off

bq query --use_legacy_sql=false < "..\sql\silver\crm_customers.sql"

bq query --use_legacy_sql=false < "..\sql\silver\crm_products.sql"

bq query --use_legacy_sql=false < "..\sql\silver\crm_sales.sql"

bq query --use_legacy_sql=false < "..\sql\silver\erp_customer_extra.sql"

bq query --use_legacy_sql=false < "..\sql\silver\erp_customer_loc.sql"

bq query --use_legacy_sql=false < "..\sql\silver\erp_product_category.sql"

echo Silver layer completed!
pause