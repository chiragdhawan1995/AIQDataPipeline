import json
import os

import psycopg2

if __name__ == "__main__":
    try:
        # Setup the connection with PG database
        with open("config/db_details.json", "r") as file:
            db_details = json.load(file)

        pg_conn = psycopg2.connect(
            user=db_details["user"],
            password=db_details["password"],
            host=db_details["host"],
            port=db_details["port"],
            database=db_details["database"],
        )
        pg_cursor = pg_conn.cursor()

        csv_file_path = os.path.join(os.getcwd(), "data\\transformed\\users_sales.csv")
        delimiter = ","  # Replace with the actual delimiter used in your CSV file

        target_tables = {
            "users_sales": "users_sales",
            "sales_per_customer": "sales_per_customer",
            "total_orders_per_product": "total_orders_per_product",
            "sorted_product_sales": "product_sales",
            "avg_sale_per_weather": "avg_sale_per_weather",
        }

        # Copy data from CSV files to Postgres tables
        for file_name, target_table in target_tables.items():
            with open(f"data/transformed/{file_name}.csv", "r") as csv_file:
                pg_cursor.copy_expert(
                    f"COPY aiq_sales.{target_table} FROM stdin WITH CSV HEADER",
                    csv_file,
                )

        # Commit the transaction
        pg_conn.commit()

        # Close the cursor and the database connection
        pg_cursor.close()
        pg_conn.close()

    except Exception as e:
        print("Exception occurred while extracting data")
        print(e)
        raise e
