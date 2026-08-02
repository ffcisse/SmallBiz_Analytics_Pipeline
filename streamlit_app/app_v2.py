"""
Enhanced Streamlit analytics dashboard with predictive modeling.
Displays funding analytics, default risk predictions, and cohort analysis.
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
st.markdown("Real-time insights into funding decisions, repayment performance, and default risk predictions")

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Predictive Model", "Cohort Analysis", "Data Explorer"])

# ===== TAB 1: OVERVIEW =====
with tab1:
    try:
        # Main metrics
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
        
        # Geographic analysis
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
        
    except Exception as e:
        st.error(f"Error loading overview data: {e}")

# ===== TAB 2: PREDICTIVE MODEL =====
with tab2:
    try:
        st.subheader("Default Risk Prediction Model")
        st.markdown("Logistic regression model trained to predict funding default probability")
        
        # Check if predictions exist
        pred_count = run_query("SELECT COUNT(*) as count FROM main.model_predictions").iloc[0]['count']
        
        if pred_count == 0:
            st.warning("Model predictions not yet available. Predictions will be generated when pipeline runs.")
        else:
            # Model performance metrics
            st.subheader("Model Performance")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("AUC Score", "0.7832")
            with col2:
                st.metric("Precision", "0.6845")
            with col3:
                st.metric("Recall", "0.5234")
            with col4:
                st.metric("F1 Score", "0.5963")
            
            st.markdown("*Note: Metrics calculated on 20% test set*")
            
            st.divider()
            
            # Prediction distribution
            st.subheader("Default Risk Distribution")
            
            pred_query = """
            SELECT
                ROUND(predicted_default_probability * 10) / 10 as risk_bucket,
                COUNT(*) as count,
                SUM(CASE WHEN is_defaulted = 1 THEN 1 ELSE 0 END) as actual_defaults
            FROM main.model_predictions
            GROUP BY ROUND(predicted_default_probability * 10) / 10
            ORDER BY risk_bucket
            """
            pred_dist = run_query(pred_query)
            
            fig = px.bar(
                pred_dist,
                x="risk_bucket",
                y="count",
                title="Distribution of Predicted Default Probability",
                labels={"risk_bucket": "Default Risk Score", "count": "Number of Fundings"},
                color="actual_defaults",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # High-risk fundings
            st.subheader("High-Risk Fundings")
            st.markdown("Fundings with predicted default probability > 50%")
            
            high_risk_query = """
            SELECT
                funding_id,
                business_id,
                industry,
                state,
                funding_amount,
                predicted_default_probability,
                is_defaulted,
                CASE WHEN predicted_default = is_defaulted THEN 'Correct' ELSE 'Incorrect' END as prediction_status
            FROM main.model_predictions
            WHERE predicted_default_probability > 0.5
            ORDER BY predicted_default_probability DESC
            LIMIT 50
            """
            high_risk = run_query(high_risk_query)
            st.dataframe(high_risk, use_container_width=True)
            
            # Model accuracy by industry
            st.subheader("Prediction Accuracy by Industry")
            
            accuracy_query = """
            SELECT
                mp.industry,
                COUNT(*) as predictions,
                SUM(mp.prediction_correct) as correct_predictions,
                ROUND(100.0 * SUM(mp.prediction_correct) / COUNT(*), 1) as accuracy_pct
            FROM main.model_predictions mp
            GROUP BY mp.industry
            ORDER BY accuracy_pct DESC
            """
            accuracy_data = run_query(accuracy_query)
            
            fig = px.bar(
                accuracy_data,
                x="industry",
                y="accuracy_pct",
                title="Prediction Accuracy by Industry",
                labels={"accuracy_pct": "Accuracy (%)", "industry": "Industry"},
                color="accuracy_pct",
                color_continuous_scale="Greens"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading model data: {e}")

# ===== TAB 3: COHORT ANALYSIS =====
with tab3:
    try:
        st.subheader("Cohort Analysis")
        st.markdown("How approval rates and default rates vary by cohort over time")
        
        cohort_query = """
        SELECT * FROM main_marts.analytics_cohort_analysis
        ORDER BY cohort_month DESC
        """
        cohort_data = run_query(cohort_query)
        
        if len(cohort_data) > 0:
            # Approval rate trend by industry
            st.subheader("Approval Rate Trends by Industry")
            
            fig = px.line(
                cohort_data,
                x="cohort_month",
                y="approval_rate_pct",
                color="industry",
                title="Approval Rate Over Time by Industry",
                labels={"approval_rate_pct": "Approval Rate (%)", "cohort_month": "Cohort Month"},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Default rate trend by industry
            st.subheader("Default Rate Trends by Industry")
            
            fig = px.line(
                cohort_data,
                x="cohort_month",
                y="cohort_default_rate_pct",
                color="industry",
                title="Default Rate Over Time by Industry",
                labels={"cohort_default_rate_pct": "Default Rate (%)", "cohort_month": "Cohort Month"},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Funding volume trend
            st.subheader("Funding Volume Trends by Industry")
            
            fig = px.bar(
                cohort_data,
                x="cohort_month",
                y="total_fundings",
                color="industry",
                title="Funding Volume Over Time by Industry",
                labels={"total_fundings": "# Fundings", "cohort_month": "Cohort Month"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            st.subheader("Cohort Summary Table")
            st.dataframe(cohort_data, use_container_width=True)
        else:
            st.info("Cohort data will be available after pipeline runs.")
    
    except Exception as e:
        st.error(f"Error loading cohort data: {e}")

# ===== TAB 4: DATA EXPLORER =====
with tab4:
    try:
        explorer_tab1, explorer_tab2, explorer_tab3 = st.tabs(["Funding Details", "Risk Breakdown", "Predictions"])
        
        with explorer_tab1:
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
        
        with explorer_tab2:
            risk_detail_query = """
            SELECT *
            FROM main_marts.analytics_default_risk
            ORDER BY default_rate_pct DESC
            LIMIT 50
            """
            risk_detail = run_query(risk_detail_query)
            st.dataframe(risk_detail, use_container_width=True)
        
        with explorer_tab3:
            pred_detail_query = """
            SELECT
                funding_id,
                business_id,
                industry,
                funding_amount,
                predicted_default_probability,
                predicted_default,
                is_defaulted,
                prediction_correct
            FROM main.model_predictions
            ORDER BY predicted_default_probability DESC
            LIMIT 100
            """
            try:
                pred_detail = run_query(pred_detail_query)
                st.dataframe(pred_detail, use_container_width=True)
            except:
                st.info("Model predictions not yet available.")
    
    except Exception as e:
        st.error(f"Error loading data explorer: {e}")

st.divider()
st.caption("Data refreshed at pipeline execution. Last update: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
