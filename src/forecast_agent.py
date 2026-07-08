import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_sales(df):
    if "Date" not in df.columns or "Sales" not in df.columns:
        return None, "Dataset must contain Date and Sales columns."

    data = df.copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.dropna(subset=["Date", "Sales"])

    daily_sales = data.groupby("Date")["Sales"].sum().reset_index()
    daily_sales = daily_sales.sort_values("Date")

    daily_sales["Day_Number"] = range(1, len(daily_sales) + 1)

    X = daily_sales[["Day_Number"]]
    y = daily_sales["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = pd.DataFrame({
        "Day_Number": range(len(daily_sales) + 1, len(daily_sales) + 8)
    })

    predictions = model.predict(future_days)

    future_dates = pd.date_range(
        start=daily_sales["Date"].max() + pd.Timedelta(days=1),
        periods=7
    )

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted Sales": predictions
    })

    return forecast_df, None