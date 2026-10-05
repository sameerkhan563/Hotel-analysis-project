import mysql.connector
import pandas as pd

try:
    print("Connecting to MySQL...")

    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="samar@sk",
        database="oyo",
        use_pure=True
    )

    print("MySQL connected successfully!\n")

    query = """
    SELECT *
    FROM `oyo_sales(oyo sql)`
    """

    df_sales = pd.read_sql(query, connection)

    print("OYO SALES DATA LOADED SUCCESSFULLY!\n")
    print("Rows:", len(df_sales))
    print("Columns:", len(df_sales.columns))

    print("\nFirst 5 Records:")
    print(df_sales.head())

    print("\nColumn Names:")
    print(df_sales.columns.tolist())


    # CITY DATA

    city_query = """
    SELECT *
    FROM `oyo_city(oyo hotels dataset)`
    """

    df_city = pd.read_sql(city_query, connection)

    print("\nOYO CITY DATA LOADED SUCCESSFULLY!")
    print("Rows:", len(df_city))
    print("Columns:", len(df_city.columns))

    print("\nCity Data:")
    print(df_city.head())

    print("\nCity Column Names:")
    print(df_city.columns.tolist())

        # DATA CLEANING

    # Remove unnecessary column
    df_sales.drop(columns=["MyUnknownColumn"], inplace=True)

    # Rename booking ID column
    df_sales.rename(
        columns={"ï»¿booking_id": "booking_id"},
        inplace=True
    )

    # Convert date columns to datetime
    df_sales["check_in"] = pd.to_datetime(df_sales["check_in"])
    df_sales["check_out"] = pd.to_datetime(df_sales["check_out"])
    df_sales["date_of_booking"] = pd.to_datetime(df_sales["date_of_booking"])

    print("\nDATA CLEANING COMPLETED!")

    print("\nSales Columns After Cleaning:")
    print(df_sales.columns.tolist())

    print("\nData Types:")
    print(df_sales.dtypes)

        # MERGE SALES AND CITY DATA

    df = pd.merge(
        df_sales,
        df_city,
        on="hotel_id",
        how="left"
    )

    print("\nDATA MERGED SUCCESSFULLY!")

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("\nFinal Columns:")
    print(df.columns.tolist())

    print("\nFinal Dataset:")
    print(df.head())

        # BASIC OYO KPIs

    total_bookings = len(df)

    total_revenue = df["amount"].sum()

    total_discount = df["discount"].sum()

    avg_booking_amount = df["amount"].mean()

    avg_rooms_per_booking = df["no_of_rooms"].mean()

    avg_stay_days = (
        df["check_out"] - df["check_in"]
    ).dt.days.mean()

    cancellation_rate = (
        (df["status"] == "Cancelled").sum()
        / total_bookings
        * 100
    )

    print("\n========== OYO BASIC KPIs ==========")

    print("Total Bookings:", total_bookings)

    print("Total Revenue:", total_revenue)

    print("Total Discount:", total_discount)

    print("Average Booking Amount:", round(avg_booking_amount, 2))

    print(
        "Average Rooms per Booking:",
        round(avg_rooms_per_booking, 2)
    )

    print(
        "Average Stay (Days):",
        round(avg_stay_days, 2)
    )

    print(
        "Cancellation Rate:",
        round(cancellation_rate, 2),
        "%"
    )

        # CITY-WISE ANALYSIS

    city_analysis = df.groupby("city").agg(
        total_bookings=("booking_id", "count"),
        total_revenue=("amount", "sum"),
        total_discount=("discount", "sum")
    ).reset_index()

    city_analysis["avg_booking_amount"] = (
        city_analysis["total_revenue"]
        / city_analysis["total_bookings"]
    )

    city_analysis = city_analysis.sort_values(
        "total_bookings",
        ascending=False
    )

    print("\n========== CITY-WISE ANALYSIS ==========")

    print(city_analysis.to_string(index=False))

        # TOP 5 CITIES BY BOOKINGS

    top_5_cities = city_analysis.head(5)

    print("\n========== TOP 5 CITIES ==========")

    print(
        top_5_cities[
            ["city", "total_bookings", "total_revenue"]
        ].to_string(index=False)
    )

        # BOOKING STATUS ANALYSIS

    status_analysis = (
        df["status"]
        .value_counts()
        .reset_index()
    )

    status_analysis.columns = ["status", "total_bookings"]

    status_analysis["percentage"] = (
        status_analysis["total_bookings"]
        / len(df)
        * 100
    )

    status_analysis["percentage"] = (
        status_analysis["percentage"].round(2)
    )

    print("\n========== BOOKING STATUS ANALYSIS ==========")

    print(
        status_analysis.to_string(index=False)
    )
        # MONTHLY ANALYSIS

    df["booking_month"] = df["date_of_booking"].dt.to_period("M")

    monthly_analysis = df.groupby("booking_month").agg(
        total_bookings=("booking_id", "count"),
        total_revenue=("amount", "sum")
    ).reset_index()

    monthly_analysis["booking_month"] = (
        monthly_analysis["booking_month"].astype(str)
    )

    print("\n========== MONTHLY ANALYSIS ==========")

    print(
        monthly_analysis.to_string(index=False)
    )
        # STAY AND ROOM ANALYSIS

    df["stay_days"] = (
        df["check_out"] - df["check_in"]
    ).dt.days

    avg_stay = df["stay_days"].mean()

    room_analysis = df.groupby("no_of_rooms").agg(
        total_bookings=("booking_id", "count"),
        total_revenue=("amount", "sum")
    ).reset_index()

    print("\n========== STAY & ROOM ANALYSIS ==========")

    print("Average Stay:", round(avg_stay, 2), "days")

    print("\nBookings by Number of Rooms:")
    print(room_analysis.to_string(index=False))

        # TOP 10 HOTELS BY REVENUE

    top_hotels = df.groupby("hotel_id").agg(
        total_bookings=("booking_id", "count"),
        total_revenue=("amount", "sum"),
        avg_booking_amount=("amount", "mean")
    ).reset_index()

    top_hotels["avg_booking_amount"] = (
        top_hotels["avg_booking_amount"].round(2)
    )

    top_hotels = top_hotels.sort_values(
        "total_revenue",
        ascending=False
    ).head(10)

    print("\n========== TOP 10 HOTELS BY REVENUE ==========")

    print(
        top_hotels.to_string(index=False)
    )
        # DISCOUNT ANALYSIS

    total_discount = df["discount"].sum()

    avg_discount_percent = (
        df["discount"] / df["amount"] * 100
    ).mean()

    df["discount_percent"] = (
        df["discount"] / df["amount"] * 100
    )

    print("\n========== DISCOUNT ANALYSIS ==========")

    print("Total Discount:", total_discount)

    print(
        "Average Discount Percentage:",
        round(avg_discount_percent, 2),
        "%"
    )
        # EXPORT FINAL DATASET

    output_file = "oyo_final_analysis.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("\n========== EXPORT COMPLETED ==========")
    print("File saved as:", output_file)

    connection.close()

    print("\nConnection closed.")

except Exception as e:
    print("ERROR:")
    print(e)