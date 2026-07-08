from typing import TypedDict
from langgraph.graph import StateGraph, END
from src.rag_agent import ask_business_data


class CEOState(TypedDict):
    context: str
    sales_metrics: str
    finance_metrics: str
    risk_metrics: str
    final_report: str


def sales_node(state: CEOState):
    state["sales_metrics"] = """
Sales Agent:
- Analyzed product-wise and city-wise sales.
- Identified top-performing and weak-performing sales areas.
"""
    return state


def finance_node(state: CEOState):
    state["finance_metrics"] = """
Finance Agent:
- Analyzed revenue, profit, and average profit.
- Identified financial strengths and weak areas.
"""
    return state


def risk_node(state: CEOState):
    state["risk_metrics"] = """
Risk Agent:
- Checked for dependency on limited products/cities.
- Checked possible business risks from low sales or low profit.
"""
    return state


def ceo_node(state: CEOState):
    combined_context = f"""
Dataset Context:
{state["context"]}

{state["sales_metrics"]}

{state["finance_metrics"]}

{state["risk_metrics"]}
"""

    final = ask_business_data(
        combined_context,
        """
Create a CEO-level executive business report.

Include:
1. Executive Summary
2. Sales Performance
3. Financial Performance
4. Risks
5. Growth Opportunities
6. Final Recommendations
"""
    )

    state["final_report"] = final
    return state


def build_ceo_graph():
    graph = StateGraph(CEOState)

    graph.add_node("sales_agent", sales_node)
    graph.add_node("finance_agent", finance_node)
    graph.add_node("risk_agent", risk_node)
    graph.add_node("ceo_agent", ceo_node)

    graph.set_entry_point("sales_agent")

    graph.add_edge("sales_agent", "finance_agent")
    graph.add_edge("finance_agent", "risk_agent")
    graph.add_edge("risk_agent", "ceo_agent")
    graph.add_edge("ceo_agent", END)

    return graph.compile()


def run_langgraph_ceo_analysis(context):
    app = build_ceo_graph()

    initial_state = {
        "context": context,
        "sales_metrics": "",
        "finance_metrics": "",
        "risk_metrics": "",
        "final_report": ""
    }

    return app.invoke(initial_state)