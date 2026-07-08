from src.rag_agent import ask_business_data


def sales_agent(context):
    question = """
Analyze the sales performance.

Tell me:
1. Best selling products
2. Worst selling products
3. Sales trend
4. Recommendations
"""
    return ask_business_data(context, question)


def finance_agent(context):
    question = """
Analyze the financial performance.

Tell me:
1. Profitability
2. High profit products
3. Low profit products
4. Financial recommendations
"""
    return ask_business_data(context, question)


def marketing_agent(context):
    question = """
Analyze customer and city performance.

Tell me:
1. Best city
2. Weakest city
3. Marketing opportunities
4. Growth suggestions
"""
    return ask_business_data(context, question)


def risk_agent(context):
    question = """
Identify business risks.

Mention:
1. Poor performing products
2. Sales risks
3. Profit risks
4. Business risks
"""
    return ask_business_data(context, question)


def forecast_agent(context):
    question = """
Based on the business data,
predict future trends and give strategic recommendations.
"""
    return ask_business_data(context, question)


def ceo_summary(
    sales,
    finance,
    marketing,
    risk,
    forecast
):

    context = f"""

Sales Analysis
{sales}

Finance Analysis
{finance}

Marketing Analysis
{marketing}

Risk Analysis
{risk}

Forecast
{forecast}

"""

    question = """
You are the CEO.

Create an executive report.

Include:

Executive Summary

Major Findings

Business Risks

Growth Opportunities

Strategic Recommendations

Final Decision
"""

    return ask_business_data(context, question)