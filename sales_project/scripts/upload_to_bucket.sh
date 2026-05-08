#!/bin/bash

# Upload CSV Files to GCS

gcloud storage cp "C:\Sreenivas\sales\sales_project\data\*.csv" gs://spalika_sales_data/data/

# Verify Uploaded Files

gcloud storage ls gs://spalika_sales_data/data/