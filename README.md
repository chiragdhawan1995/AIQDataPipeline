### Extract
* This script ingests the 3 data sets - Users, Sales and Weather data
* The user data is available in a CSV file under data/source/sales.csv
* For the sales data we hit the API https://jsonplaceholder.typicode.com/users
* Using the latitude and longitude values, we get the weather details from the openweathermap API
* The data is ingested using `Pandas` library and the merged dataset is dumped as a CSV
* The merged dataset is available under data/transformed/users_sales.csv

### Analysis
* Using the merged dataset, we calculate different metrics such as top 5 metrics, sales across different months, etc.
* All the metrics calculated are dumped as CSV files under the directory data/transformed

### Load
* This script is used to load the merged dataset and calculated metrics into a Postgres database
* For doing this, we use `psycopg2` library. The CSV files are directly loaded to Postgres

### Setup
* Configure a PG database
* The details for the database should be stored under config/db_details.json
* The file locations have to be captured file_locations.json. File locations can be defined in different ways depending on the platform on which the scripts are being run
* Install the following libraries - `pandas`, `psycopg2`, `requests`
* Run the scripts in the following order - `extract`, `analysis` and `load`
