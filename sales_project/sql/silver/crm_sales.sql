create table silver_sales_ds.crm_sales (
	sls_ord_num string,
	sls_prd_key string,
	sls_cust_id string,
	sls_order_dt date,
	sls_ship_dt date,
	sls_due_dt date,
	sls_sales float64,
	sls_quantity int64,
	sls_price float64,
	sls_sales_calc float64,
	ingestion_dt TIMESTAMP
	)
