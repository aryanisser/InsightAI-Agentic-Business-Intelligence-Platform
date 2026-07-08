def generate_business_insights(df):
    insights = []

    if "Sales" in df.columns:
        total_sales = df["Sales"].sum()
        avg_sales = df["Sales"].mean()
        insights.append(f"Total sales generated: ₹{total_sales:,.0f}")
        insights.append(f"Average sales per order: ₹{avg_sales:,.0f}")

    if "Profit" in df.columns:
        total_profit = df["Profit"].sum()
        avg_profit = df["Profit"].mean()
        insights.append(f"Total profit earned: ₹{total_profit:,.0f}")
        insights.append(f"Average profit per order: ₹{avg_profit:,.0f}")

    if "Product" in df.columns and "Sales" in df.columns:
        top_product = df.groupby("Product")["Sales"].sum().idxmax()
        low_product = df.groupby("Product")["Sales"].sum().idxmin()
        insights.append(f"Best performing product: {top_product}")
        insights.append(f"Lowest performing product: {low_product}")

    if "City" in df.columns and "Sales" in df.columns:
        top_city = df.groupby("City")["Sales"].sum().idxmax()
        insights.append(f"Highest revenue city: {top_city}")

    if "Quantity" in df.columns:
        total_quantity = df["Quantity"].sum()
        insights.append(f"Total units sold: {total_quantity}")

    recommendations = [
        "Increase stock for best-performing products.",
        "Run discounts or campaigns for low-performing products.",
        "Focus marketing efforts on high-revenue cities.",
        "Track profit margins regularly to improve business decisions."
    ]

    return insights, recommendations