# Small Business Funding Data Pipeline

A production-grade data engineering portfolio project demonstrating end-to-end pipelines for real-world applications. This project models small business funding decisions and repayment risk using synthetic data, complete with orchestration, testing, and CI/CD.

## Architecture

**Data Flow:** Synthetic funding & repayment data → DuckDB → dbt (staging/marts/tests) → Dagster orchestration → Streamlit analytics dashboard

**Stack:** DuckDB, dbt, Dagster, Streamlit, Docker, GitHub Actions, Python

## Key Features

- **Complete pipeline:** Data ingestion through analytics dashboard, not isolated notebooks
- **Data quality:** Automated dbt tests running on every commit via GitHub Actions
- **Production practices:** Containerized with Docker, orchestrated with Dagster, version controlled
- **Business domain:** Small business funding decisions with real analytical questions
  - Default rates by industry
  - Repayment risk by segment
  - Funding decision patterns
- **Reproducible:** One-weekend build from scratch; runs locally or in containers

## Project Structure

```
small-business-funding-pipeline/
├── data/
│   ├── raw/                 # Generated synthetic data
│   └── processed/           # Intermediate processed data
├── dbt/
│   ├── models/
│   │   ├── staging/         # Raw data transformations
│   │   └── marts/           # Business-ready analytics models
│   ├── tests/               # dbt data quality tests
│   ├── dbt_project.yml
│   └── profiles.yml
├── dagster/
│   ├── definitions.py       # Dagster job & asset definitions
│   └── __init__.py
├── streamlit_app/
│   └── app.py               # Streamlit analytics dashboard
├── scripts/
│   └── generate_data.py     # Synthetic data generation
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/workflows/
    └── dbt-test.yml         # CI/CD pipeline
```

## Quick Start

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/small-business-funding-pipeline.git
   cd small-business-funding-pipeline
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate synthetic data**
   ```bash
   python scripts/generate_data.py
   ```

5. **Run dbt models**
   ```bash
   cd dbt
   dbt run
   dbt test
   ```

6. **Start Dagster UI** (optional)
   ```bash
   dagster dev
   ```

7. **Run Streamlit dashboard**
   ```bash
   streamlit run streamlit_app/app.py
   ```

### Docker Setup

```bash
docker compose up
```

This runs:
- DuckDB database
- dbt models
- Dagster orchestration
- Streamlit dashboard (accessible at http://localhost:8501)

## Data Model

### Businesses
- Business ID, industry, founding date, employee count
- Location (state)

### Funding Decisions
- Funding ID, business ID, funding amount, decision (approved/denied)
- Decision date, decision factors

### Repayment Status
- Repayment ID, funding ID, repayment date
- Status (current, 30/60/90+ days late, defaulted)

## dbt Models

### Staging Layer (`staging/`)
- `stg_businesses.sql` – Cleansed business data
- `stg_funding_decisions.sql` – Cleansed funding applications
- `stg_repayments.sql` – Cleansed repayment records

### Mart Layer (`marts/`)
- `fct_funding_decisions.sql` – Fact table for funding events
- `dim_businesses.sql` – Dimension table for business attributes
- `analytics_default_risk.sql` – Analytics: default rates by segment

## Testing

Run dbt tests:
```bash
cd dbt
dbt test
```

Run Python tests:
```bash
pytest
```

## CI/CD

GitHub Actions workflow (`.github/workflows/dbt-test.yml`) runs on every push:
- Installs dependencies
- Generates data
- Runs dbt tests
- Reports test results

## Next Steps

- [ ] Generate synthetic data (`scripts/generate_data.py`)
- [ ] Build dbt staging models
- [ ] Build dbt mart models
- [ ] Add dbt tests
- [ ] Create Dagster jobs
- [ ] Build Streamlit dashboard
- [ ] Dockerize everything
- [ ] Set up GitHub Actions

## Built By

A weekend portfolio project demonstrating real data engineering skills for data analyst, data scientist, and ML engineering roles.
