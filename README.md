# Small Business Funding Data Pipeline

A production-grade data engineering portfolio project demonstrating end-to-end pipelines for real-world applications. This project models small business funding decisions and repayment risk using synthetic data, complete with ML modeling, testing, and CI/CD.

## Architecture

**Data Flow:** Synthetic funding & repayment data → DuckDB → dbt (staging/marts/tests) → scikit-learn predictions → Streamlit analytics dashboard

**Stack:** DuckDB, dbt, Python, scikit-learn, Streamlit, Docker, GitHub Actions, Plotly

## Key Features

- **Complete pipeline:** Data ingestion through analytics dashboard, not isolated notebooks
- **Data quality:** 21 automated dbt tests running on every commit via GitHub Actions
- **Production practices:** Containerized with Docker, version controlled, reproducible
- **Business domain:** Small business funding decisions with real analytical questions
  - Default rates by industry and segment
  - Repayment risk classification
  - Cohort analysis of approval trends over time
- **Predictive modeling:** Logistic regression classifier predicting funding default probability
- **Professional dashboard:** 4-tab analytics interface with visualizations and data explorer
- **Reproducible:** One-weekend build from scratch; runs with single Docker command

## Quick Start

### Docker (Recommended)

```bash
git clone https://github.com/ffcisse/SmallBiz_Analytics_Pipeline.git
cd SmallBiz_Analytics_Pipeline
docker compose up --build
```

Open **http://localhost:8501**

### Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/generate_data.py
cd dbt && dbt run --profiles-dir . && dbt test --profiles-dir .
cd .. && python scripts/train_model.py
streamlit run streamlit_app/app_v2.py
```

## Data Model

- **500 businesses** with industry, location, employee count, annual revenue
- **800 funding decisions** with approval, amounts, interest rates
- **564 repayments** with status tracking (current/late/defaulted)

### dbt Transformations

**Staging:** 3 views cleaning and standardizing raw data
**Marts:** 3 tables for analytics (fact table, default rates, cohort analysis)

## Machine Learning

**Default Risk Classifier**
- Model: Logistic Regression (scikit-learn)
- Features: 10 engineered features (funding amount, employee count, revenue ratios, log transforms)
- Training: 80-20 split with StandardScaler normalization
- Output: Default probability predictions for 564+ approved fundings

## Dashboard (4 Tabs)

1. **Overview** — Key metrics, industry analysis, risk segments, approval trends, geographic breakdown
2. **Predictive Model** — Model performance, default risk distribution, high-risk fundings, accuracy by industry
3. **Cohort Analysis** — Approval/default rate trends over time by industry, funding volume trends
4. **Data Explorer** — Detailed funding records, risk breakdown, model predictions

## Data Quality

21 automated dbt tests covering uniqueness, not-null constraints, accepted values, referential integrity

**CI/CD:** GitHub Actions runs all tests on every push to main

## Technologies

- **Database:** DuckDB
- **Transformations:** dbt 1.7
- **ML/Feature Engineering:** scikit-learn, Python
- **Analytics & Visualization:** Streamlit, Plotly
- **Containerization:** Docker, Docker Compose
- **Version Control & CI/CD:** GitHub, GitHub Actions

## Development

### Add New dbt Models
```bash
cd dbt
dbt run --profiles-dir .
dbt test --profiles-dir .
```

### Modify Dashboard
Edit `streamlit_app/app_v2.py` — auto-reloads on save

### Generate New Data
Edit `scripts/generate_data.py` and run:
```bash
python scripts/generate_data.py
```

## Deployment

### Heroku
```bash
echo "web: streamlit run streamlit_app/app_v2.py" > Procfile
git push heroku main
```

## Portfolio Value

Demonstrates:
- Data Engineering: Full pipeline with dbt data modeling
- Software Engineering: Testing, CI/CD, version control, Docker
- Machine Learning: Feature engineering, model training, predictions
- Analytics: Dashboard design, cohort analysis, business insights
- Production Practices: Reproducible, scalable, testable code

## Author

Built by Farah Cisse (UC Berkeley, Data Science & Bioengineering)

- GitHub: [@ffcisse](https://github.com/ffcisse)
- LinkedIn: [farah-cisse](https://www.linkedin.com/in/farah-cisse)
- Email: ffcisse@berkeley.edu

## License

Open source — freely available for learning and portfolio purposes
