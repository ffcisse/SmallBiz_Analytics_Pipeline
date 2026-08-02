"""
Streamlit analytics dashboard for small business funding pipeline.
Displays funding decisions, repayment status, and risk analysis.
"""

import os
import duckdb
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Funding Pipeline Analytics",
    page_icon="📊",
    layout="wide"
)

# Professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    h1, h2, h3 {
        font-weight: 600;
        letter-spacing: -0.5px;
    }
</style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_connection():
    db_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "funding_pipeline.duckdb"
    )
    return duckdb.connect(db_path)

conn = get_connection()

# Helper function to run queries
@st.cache_data
def run_query(query: str) -> pd.DataFrame:
    return conn.execute(query).df()

# Page title
st.title("Small Business Funding Analytics")
st.markdown("Real-time insights into funding decisions and repayment performance")

# Load data
try:
    # Main metrics query
    metrics_query = """
    SELECT
        count(*) as total_fundings,
        sum(case when decision = 'approved' then 1 else 0 end) as approved_count,
        sum(case when decision = 'denied' then 1 else 1 end) as denied_count,
        round(100.0 * sum(case when decision = 'approved' then 1 else 0 end) / count(*), 1) as approval_rate,
        sum(case when is_defaulted = 1 then 1 else 0 end) as default_count,
        round(100.0 * sum(case when is_defaulted = 1 then 1 else 0 end) / 
              nullif(sum(case when decision = 'approved' then 1 else 0 end), 0), 1) as default_rate
    FROM main_marts.fct_funding_decisions
    """
    metrics = run_query(metrics_query).to_dict('records')[0]
    
    # Display key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Fundings", f"{metrics['total_fundings']:,}")
    with col2:
        st.metric("Approval Rate", f"{metrics['approval_rate']:.1f}%")
    with col3:
        st.metric("Approved", f"{metrics['approved_count']:,}")
    with col4:
        st.metric("Defaults", f"{metrics['default_count']:,}")
    with col5:
        st.metric("Default Rate", f"{metrics['default_rate']:.1f}%")
    
    st.divider()
    
    # Default rates by industry
    st.subheader("Default Rates by Industry")
    industry_query = """
    SELECT
        industry,
        count(*) as total_fundings,
        sum(case when is_defaulted = 1 then 1 else 0 end) as defaults,
        round(100.0 * sum(case when is_defaulted = 1 then 1 else 0 end) / count(*), 2) as default_rate
    FROM main_marts.fct_funding_decisions
    WHERE decision = 'approved'
    GROUP BY industry
    ORDER BY default_rate DESC
    """
    industry_data = run_query(industry_query)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            industry_data,
            x="industry",
            y="default_rate",
            title="Default Rate by Industry",
            labels={"default_rate": "Default Rate (%)", "industry": "Industry"},
            color="default_rate",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            industry_data,
            x="industry",
            y="total_fundings",
            title="Funding Volume by Industry",
            labels={"total_fundings": "# Fundings", "industry": "Industry"},
            color="total_fundings",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk segment analysis
    st.subheader("Risk Segment Analysis")
    risk_query = """
    SELECT
        risk_segment,
        count(*) as count,
        round(avg(funding_amount), 0) as avg_funding,
        round(100.0 * sum(case when is_defaulted = 1 then 1 else 0 end) / count(*), 2) as default_rate
    FROM main_marts.fct_funding_decisions
    WHERE decision = 'approved'
    GROUP BY risk_segment
    ORDER BY default_rate DESC
    """
    risk_data = run_query(risk_query)
    
    fig = px.bar(
        risk_data,
        x="risk_segment",
        y="count",
        title="Loan Count by Risk Segment",
        labels={"count": "# Loans", "risk_segment": "Risk Segment"},
        color="default_rate",
        color_continuous_scale="RdYlGn_r",
        hover_data={"avg_funding": True, "default_rate": True}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Approval trends
    st.subheader("Approval Trends")
    approval_query = """
    SELECT
        decision_date,
        decision,
        count(*) as count
    FROM main_marts.fct_funding_decisions
    GROUP BY decision_date, decision
    ORDER BY decision_date
    """
    approval_data = run_query(approval_query)
    
    fig = px.line(
        approval_data,
        x="decision_date",
        y="count",
        color="decision",
        title="Funding Decisions Over Time",
        labels={"count": "# Decisions", "decision_date": "Decision Date"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # State analysis
    st.subheader("Geographic Analysis")
    state_query = """
    SELECT
        state,
        count(*) as total_fundings,
        sum(case when decision = 'approved' then 1 else 0 end) as approved,
        round(100.0 * sum(case when is_defaulted = 1 then 1 else 0 end) / count(*), 2) as default_rate
    FROM main_marts.fct_funding_decisions
    GROUP BY state
    ORDER BY total_fundings DESC
    LIMIT 10
    """
    state_data = run_query(state_query)
    
    fig = px.bar(
        state_data,
        x="state",
        y="total_fundings",
        title="Top 10 States by Funding Volume",
        labels={"total_fundings": "# Fundings", "state": "State"},
        color="default_rate",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Data explorer
    st.subheader("Data Explorer")
    
    tab1, tab2 = st.tabs(["Funding Details", "Risk Breakdown"])
    
    with tab1:
        detail_query = """
        SELECT
            funding_id,
            business_name,
            industry,
            state,
            funding_amount,
            decision,
            interest_rate,
            repayment_status,
            is_defaulted
        FROM main_marts.fct_funding_decisions
        ORDER BY decision_date DESC
        LIMIT 100
        """
        detail_data = run_query(detail_query)
        st.dataframe(detail_data, use_container_width=True)
    
    with tab2:
        risk_detail_query = """
        SELECT *
        FROM main_marts.analytics_default_risk
        ORDER BY default_rate_pct DESC
        LIMIT 50
        """
        risk_detail = run_query(risk_detail_query)
        st.dataframe(risk_detail, use_container_width=True)
    
    st.divider()
    st.caption("Data refreshed at pipeline execution. Last update: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Make sure the pipeline has been run and data is available in DuckDB.")
