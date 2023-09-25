import json

import pandas as pd
import requests


def get_data_from_csv(file_location: str) -> pd.DataFrame:
    """
    Read data from a CSV file into a Pandas Dataframe
    @param file_location: Location of CSV file
    @return: Pandas DF created from CSV data
    """

    df_from_csv = pd.read_csv(file_location)
    return df_from_csv


def get_data_from_api(api_endpoint: str) -> dict:
    """
    Hit the API and the return the response as a dictionary
    @param api_endpoint: URL of the API
    @return: Response from API
    """

    response = requests.get(api_endpoint)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(
            f"Failed to retrieve data from API. " f"Status code: {response.status_code}"
        )


def get_flattened_user_data(users_dict: dict) -> dict:
    """
    The users data returned by API is nested. This functions is to parse it.
    @param users_dict: Dictionary with the user details
    @return: List of user details flattened out
    """

    users_data_list = []

    for user in users_dict:
        users_data_list.append(
            {
                "id": user["id"],
                "name": user["name"],
                "username": user["username"],
                "email": user["email"],
                "lat": user["address"]["geo"]["lat"],
                "lng": user["address"]["geo"]["lng"],
            }
        )

    return users_data_list


def get_weather_details(lat: float, lon: float) -> tuple[float, str]:
    """
    Hit the openweathermap API to get weather details using
    latitude and longitude.
    @param lat: Latitude
    @param lon: Longitude
    @return: The temperature and weather description
    """

    app_id = "2f0262b1d25dd4b3b8b1406a2c887b5a"
    weather_api = (
        "https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={app_id}"
    )

    weather_dict = get_data_from_api(weather_api)
    temp = weather_dict["main"]["temp"]
    weather_desc = weather_dict["weather"][0]["description"]
    return temp, weather_desc


if __name__ == "__main__":
    try:
        with open("config/file_locations.json", "r") as file:
            file_locations = json.load(file)

        # Get sales data from CSV into a DF
        sales_data_csv_loc = file_locations["sales_data_csv_loc"]
        sales_df = get_data_from_csv(sales_data_csv_loc)

        # Get user details from the API
        user_api = "https://jsonplaceholder.typicode.com/users"
        users_dict = get_data_from_api(user_api)

        # Flatten out the nested data
        flat_user_data = get_flattened_user_data(users_dict)
        user_df = pd.DataFrame(flat_user_data)

        # Merge the user and sales data
        users_sales_df = pd.merge(
            sales_df, user_df, left_on="customer_id", right_on="id", how="inner"
        )
        users_sales_df = users_sales_df.drop(columns="id")

        # Get the temp and weather for each record
        users_sales_df[["temp", "weather_desc"]] = users_sales_df.apply(
            lambda row: pd.Series(get_weather_details(row["lat"], row["lng"])), axis=1
        )

        # Dump the data to a CSV
        users_sales_df.to_csv(
            file_locations["users_sales_csv_loc"], index=False, header=True, mode="w"
        )

    except Exception as e:
        print("Exception occurred while extracting data")
        print(e)
        raise e
