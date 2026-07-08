import pandas as pd

def detect_anomalies(df):
    if "Date" not in df.columns or "Sales" not in df.columns:
        return None, "Dataset must contain Date and Sales columns."

    data = df.copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.dropna(subset=["Date", "Sales"])

    daily_sales = data.groupby("Date")["Sales"].sum().reset_index()

    mean_sales = daily_sales["Sales"].mean()
    std_sales = daily_sales["Sales"].std()

    daily_sales["Anomaly"] = daily_sales["Sales"].apply(
        lambda x: "Anomaly" if x > mean_sales + 2 * std_sales or x < mean_sales - 2 * std_sales else "Normal"
    )

    anomalies = daily_sales[daily_sales["Anomaly"] == "Anomaly"]

    return anomalies, None