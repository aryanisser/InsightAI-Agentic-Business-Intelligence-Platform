from src.langgraph_ceo_agent import run_langgraph_ceo_analysis
from src.ceo_agent import *
from src.real_rag import create_rag_collection, retrieve_context
from src.rag_agent import ask_business_data
from src.report_generator import generate_ceo_pdf
from src.insight_agent import generate_business_insights
from src.anomaly_agent import detect_anomalies
from src.forecast_agent import forecast_sales
from src.data_cleaner import clean_data
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="InsightAI - Business Intelligence System", layout="wide")

st.sidebar.title("📊 InsightAI")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Data Cleaning", "EDA", "Forecast","Anomaly Detection", "AI Insights", "AI Chat","AI CEO Mode","LangGraph CEO Mode", "Reports"]
)

st.title("InsightAI - Agentic Business Intelligence System")
st.write("Upload your business dataset and get automatic insights, charts, forecasting, and AI analysis.")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is None:
    st.info("Please upload a CSV or Excel file to continue.")
    st.stop()

try:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if df.empty:
        st.error("Uploaded file is empty.")
        st.stop()

except Exception as e:
    st.error(f"File reading error: {e}")
    st.stop()

df, cleaning_report = clean_data(df)

st.success("File uploaded successfully!")

if page == "Dashboard":
    st.header("Business Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"₹{df['Sales'].sum():,.0f}")
    col2.metric("Total Profit", f"₹{df['Profit'].sum():,.0f}")
    col3.metric("Total Orders", len(df))
    col4.metric("Average Profit", f"₹{df['Profit'].mean():,.0f}")

    sales_product = df.groupby("Product")["Sales"].sum().reset_index()
    fig = px.bar(sales_product, x="Product", y="Sales", title="Sales by Product")
    st.plotly_chart(fig, use_container_width=True)

    profit_city = df.groupby("City")["Profit"].sum().reset_index()
    fig = px.pie(profit_city, names="City", values="Profit", title="Profit Distribution by City")
    st.plotly_chart(fig, use_container_width=True)

    trend = df.groupby("Date")["Sales"].sum().reset_index()
    fig = px.line(trend, x="Date", y="Sales", markers=True, title="Sales Trend")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Data Cleaning":
    st.header("Smart Data Cleaning Report")
    for item in cleaning_report:
        st.success(item)

    st.subheader("Cleaned Dataset Preview")
    st.dataframe(df.head())

elif page == "EDA":
    st.header("Exploratory Data Analysis")

    st.subheader("Dataset Information")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))

    st.subheader("Column Summary")
    st.dataframe(df.describe(include="all"))

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if numeric_cols:
        selected_col = st.selectbox("Select numeric column", numeric_cols)

        fig = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
        st.plotly_chart(fig, use_container_width=True)

        corr = df[numeric_cols].corr()
        fig_corr = px.imshow(corr, text_auto=True, title="Correlation Between Numeric Columns")
        st.plotly_chart(fig_corr, use_container_width=True)

elif page == "Anomaly Detection":
    st.header("Anomaly Detection")

    anomalies, error = detect_anomalies(df)

    if error:
        st.error(error)
    elif anomalies.empty:
        st.success("No major sales anomalies detected.")
    else:
        st.warning("Sales anomalies detected:")
        st.dataframe(anomalies)        

elif page == "AI Insights":
    st.header("AI Business Insights")

    if st.button("✨ Generate AI Business Insights"):
        insights, recommendations = generate_business_insights(df)

        st.subheader("Key Insights")
        for insight in insights:
            st.success(insight)

        st.subheader("Business Recommendations")
        for rec in recommendations:
            st.info(rec)

elif page == "Forecast":
    st.header("Sales Forecasting")

    forecast_df, error = forecast_sales(df)

    if error:
        st.error(error)
    else:
        st.subheader("Next 7 Days Sales Prediction")
        st.dataframe(forecast_df)

        fig = px.line(
            forecast_df,
            x="Date",
            y="Predicted Sales",
            markers=True,
            title="7-Day Sales Forecast"
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "AI Chat":
    st.header("Chat with Your Business Data")

    if "rag_collection" not in st.session_state:
        with st.spinner("Creating RAG vector database..."):
            st.session_state.rag_collection = create_rag_collection(df)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.text_input("Ask a question about your uploaded dataset")

    if st.button("Ask AI"):
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching relevant business data..."):
                context = retrieve_context(
                    st.session_state.rag_collection,
                    question
                )

            with st.spinner("AI is analyzing retrieved context..."):
                answer = ask_business_data(context, question)

            st.session_state.chat_history.append(("You", question))
            st.session_state.chat_history.append(("AI", answer))

    st.subheader("Chat History")

    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.write(f"**You:** {message}")
        else:
            st.write(f"**AI:** {message}")

elif page == "AI CEO Mode":
    
    st.header("👔 AI CEO Business Consultant")

    if "rag_collection" not in st.session_state:
        with st.spinner("Creating RAG vector database..."):
            st.session_state.rag_collection = create_rag_collection(df)

    ceo_question = """
    Analyze this business dataset like a CEO.
    Include sales performance, profit performance, city performance,
    product performance, risks, opportunities, and final recommendations.
    """

    if st.button("Analyze My Business"):

        with st.spinner("Retrieving business context..."):
            ceo_context = retrieve_context(
                st.session_state.rag_collection,
                ceo_question,
                top_k=10
            )

        with st.spinner("Generating CEO report..."):
            report = ask_business_data(ceo_context, ceo_question)

        st.success("CEO Report Generated")

        st.subheader("👔 CEO Executive Report")
        st.write(report)

        pdf_path = generate_ceo_pdf(report)

        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download CEO Report PDF",
                data=file,
                file_name="ceo_business_report.pdf",
                mime="application/pdf"
            )

elif page == "LangGraph CEO Mode":
    
    st.header("🧠 LangGraph Multi-Agent CEO System")

    if "rag_collection" not in st.session_state:
        with st.spinner("Creating RAG vector database..."):
            st.session_state.rag_collection = create_rag_collection(df)

    ceo_question = """
    Analyze the complete business dataset for sales, finance, risk, and future growth.
    """

    if st.button("Run LangGraph CEO Analysis"):

        with st.spinner("Retrieving business context..."):
            ceo_context = retrieve_context(
                st.session_state.rag_collection,
                ceo_question,
                top_k=10
            )

        with st.spinner("Running LangGraph workflow..."):
            result = run_langgraph_ceo_analysis(ceo_context)

        st.success("LangGraph Analysis Complete")

        with st.expander("📈 Sales Agent"):
            st.write(result["sales_metrics"])

        with st.expander("💰 Finance Agent"):
            st.write(result["finance_metrics"])

        with st.expander("⚠ Risk Agent"):
            st.write(result["risk_metrics"])

        st.divider()

        st.subheader("👔 Final CEO Executive Report")
        st.write(result["final_report"])

        pdf_path = generate_ceo_pdf(result["final_report"])

        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download LangGraph CEO Report PDF",
                data=file,
                file_name="langgraph_ceo_report.pdf",
                mime="application/pdf"
            )


elif page == "Reports":
    
    st.header("📄 Business Report Center")

    insights, recommendations = generate_business_insights(df)

    st.subheader("Report Preview")

    st.write("### Key Insights")
    for insight in insights:
        st.success(insight)

    st.write("### Recommendations")
    for rec in recommendations:
        st.info(rec)

    if st.button("Generate Business Report PDF"):

        report_text = "InsightAI Business Report\n\n"

        report_text += "Key Insights:\n"
        for insight in insights:
            report_text += f"- {insight}\n"

        report_text += "\nRecommendations:\n"
        for rec in recommendations:
            report_text += f"- {rec}\n"

        pdf_path = generate_ceo_pdf(report_text)

        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download Business Report PDF",
                data=file,
                file_name="business_report.pdf",
                mime="application/pdf"
            )            