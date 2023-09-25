import json

import pandas as pd

if __name__ == "__main__":
    try:
        with open("config/file_locations.json", "r") as file:
            file_locations = json.load(file)

        users_sales_df = pd.read_csv(file_locations["users_sales_csv_loc"])

        # Total sales amount per customer
        sales_per_customer_df = (
            users_sales_df.groupby("customer_id")["price"].sum().reset_index()
        )
        sales_per_customer_df.rename(columns={"price": "total_sale"}, inplace=True)
        sales_per_customer_df.to_csv(
            file_locations["sales_per_customer_csv_loc"],
            index=False,
            header=True,
            mode="w",
        )

        # Total average quantity per product(average was not possible)
        total_orders_per_product_df = (
            users_sales_df.groupby("product_id")["order_id"].nunique().reset_index()
        )
        total_orders_per_product_df.rename(
            columns={"order_id": "total_orders"}, inplace=True
        )
        total_orders_per_product_df.to_csv(
            file_locations["total_orders_per_product_csv_loc"],
            index=False,
            header=True,
            mode="w",
        )

        # Top 5 products
        product_sales_df = users_sales_df["product_id"].value_counts().reset_index()
        product_sales_df.rename(columns={"count": "sales_count"}, inplace=True)
        sorted_product_sales_df = product_sales_df.sort_values(
            by="sales_count", ascending=False
        ).head(5)
        sorted_product_sales_df.to_csv(
            file_locations["sorted_product_sales_csv_loc"],
            index=False,
            header=True,
            mode="w",
        )

        # Sales trend by month
        users_sales_df["order_date"] = pd.to_datetime(users_sales_df["order_date"])
        users_sales_df["sale_month"] = users_sales_df["order_date"].dt.month
        users_sales_df["sale_year"] = users_sales_df["order_date"].dt.year
        sale_per_month_df = (
            users_sales_df.groupby(["sale_year", "sale_month"])["price"]
            .sum()
            .reset_index()
        )
        sale_per_month_df.rename(columns={"price": "total_sale"}, inplace=True)
        sale_per_month_df.to_csv(
            file_locations["sale_per_month_csv_loc"], index=False, header=True, mode="w"
        )

        # Average sale per weather condition
        avg_sale_per_weather_df = (
            users_sales_df.groupby("weather_desc")["price"].mean().reset_index()
        )
        avg_sale_per_weather_df.rename(columns={"price": "avg_sale"}, inplace=True)
        avg_sale_per_weather_df.to_csv(
            file_locations["avg_sale_per_weather_csv_loc"],
            index=False,
            header=True,
            mode="w",
        )

    except Exception as e:
        print("Exception occurred while extracting data")
        print(e)
        raise e
