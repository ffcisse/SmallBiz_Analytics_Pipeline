# Quick Start Guide

Get the funding pipeline up and running in minutes.

## Option 1: Local Setup (Recommended for Development)

### 1. Clone & Setup
```bash
git clone https://github.com/YOUR-USERNAME/small-business-funding-pipeline.git
cd small-business-funding-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Data
```bash
python scripts/generate_data.py
```
This creates a DuckDB database with synthetic funding and repayment data.

### 3. Run dbt Pipeline
```bash
cd dbt

# Run models
dbt run --profiles-dir .

# Run data quality tests
dbt test --profiles-dir .
```

### 4. View Results in Streamlit
```bash
cd ..
streamlit run streamlit_app/app.py
```
Open http://localhost:8501 in your browser.

### 5. (Optional) Explore with Dagster
In a separate terminal:
```bash
dagster dev
```
Open http://localhost:3000 for the Dagster UI.

## Option 2: Docker Setup (One Command)

```bash
docker compose up
```

This will:
1. Generate synthetic data
2. Run dbt models
3. Run data quality tests
4. Start the Streamlit dashboard at http://localhost:8501

## Project Workflow

```
1. Generate Data
   └─ scripts/generate_data.py creates DuckDB database

2. Transform Data (dbt)
   ├─ Staging Layer: Clean and standardize raw data
   ├─ Marts Layer: Create fact tables and analytics views
   └─ Tests: Run 20+ data quality checks

3. Orchestrate (Dagster - Optional)
   └─ Manages job dependencies and scheduling

4. Visualize (Streamlit)
   └─ Dashboard with analytics and KPIs
```

## Key Files to Explore

- **`scripts/generate_data.py`** - Data generation logic
- **`dbt/models/`** - All SQL transformations
- **`dagster/definitions.py`** - Pipeline orchestration
- **`streamlit_app/app.py`** - Analytics dashboard
- **`.github/workflows/dbt-test.yml`** - CI/CD configuration

## Troubleshooting

### dbt can't find profiles
```bash
cd dbt
dbt run --profiles-dir .
```

### DuckDB database not found
```bash
python scripts/generate_data.py
```

### Streamlit port already in use
```bash
streamlit run streamlit_app/app.py --server.port 8502
```

### Docker build fails
```bash
docker compose build --no-cache
docker compose up
```

## Next Steps

- [ ] Customize the synthetic data (adjust INDUSTRIES, employee counts, etc.)
- [ ] Add more dbt tests for stricter data quality
- [ ] Build additional Streamlit visualizations
- [ ] Set up Dagster scheduling for periodic runs
- [ ] Deploy to production (e.g., Heroku, AWS)

## Commands Cheat Sheet

| Task | Command |
|------|---------|
| Generate data | `python scripts/generate_data.py` |
| Run dbt models | `cd dbt && dbt run --profiles-dir .` |
| Run dbt tests | `cd dbt && dbt test --profiles-dir .` |
| Start dashboard | `streamlit run streamlit_app/app.py` |
| Start Dagster | `dagster dev` |
| Run everything | `docker compose up` |

## Questions?

- Check README.md for architecture overview
- Review individual model comments in `dbt/models/`
- Explore dbt docs: `cd dbt && dbt docs serve`
