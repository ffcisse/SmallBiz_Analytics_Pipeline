"""
Dagster job and asset definitions for the funding pipeline.
Orchestrates data generation, dbt models, and analytics.
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path

from dagster import (
    Definitions,
    graph,
    op,
    In,
    Out,
    DynamicOut,
    DynamicOutput,
    Field,
    String,
    job,
)


@op(config_schema={"data_dir": Field(String, default_value="data")})
def generate_synthetic_data(context) -> str:
    """Generate synthetic funding and repayment data."""
    context.log.info("Starting synthetic data generation...")
    
    script_path = Path(__file__).parent.parent / "scripts" / "generate_data.py"
    
    try:
        result = subprocess.run(
            ["python", str(script_path)],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
            check=True
        )
        context.log.info(result.stdout)
        context.log.info("✓ Synthetic data generation complete")
        return "data_generated"
    except subprocess.CalledProcessError as e:
        context.log.error(f"Data generation failed: {e.stderr}")
        raise


@op
def run_dbt_staging(context) -> str:
    """Run dbt staging models."""
    context.log.info("Running dbt staging models...")
    
    dbt_project_path = Path(__file__).parent.parent / "dbt"
    
    try:
        result = subprocess.run(
            ["dbt", "run", "--models", "tag:staging", "--profiles-dir", "."],
            cwd=dbt_project_path,
            capture_output=True,
            text=True,
            check=True
        )
        context.log.info(result.stdout)
        context.log.info("✓ Staging models complete")
        return "staging_complete"
    except subprocess.CalledProcessError as e:
        context.log.error(f"dbt staging failed: {e.stderr}")
        raise


@op
def run_dbt_marts(context) -> str:
    """Run dbt mart models."""
    context.log.info("Running dbt mart models...")
    
    dbt_project_path = Path(__file__).parent.parent / "dbt"
    
    try:
        result = subprocess.run(
            ["dbt", "run", "--models", "tag:marts", "--profiles-dir", "."],
            cwd=dbt_project_path,
            capture_output=True,
            text=True,
            check=True
        )
        context.log.info(result.stdout)
        context.log.info("✓ Mart models complete")
        return "marts_complete"
    except subprocess.CalledProcessError as e:
        context.log.error(f"dbt marts failed: {e.stderr}")
        raise


@op
def run_dbt_tests(context, upstream: str) -> str:
    """Run dbt data quality tests."""
    context.log.info("Running dbt tests...")
    
    dbt_project_path = Path(__file__).parent.parent / "dbt"
    
    try:
        result = subprocess.run(
            ["dbt", "test", "--profiles-dir", "."],
            cwd=dbt_project_path,
            capture_output=True,
            text=True,
            check=True
        )
        context.log.info(result.stdout)
        context.log.info("✓ All tests passed")
        return "tests_passed"
    except subprocess.CalledProcessError as e:
        context.log.error(f"dbt tests failed: {e.stderr}")
        raise


@graph
def funding_pipeline_graph():
    """Complete funding pipeline orchestration."""
    data = generate_synthetic_data()
    staging = run_dbt_staging()
    marts = run_dbt_marts()
    tests = run_dbt_tests(marts)
    return tests


funding_pipeline_job = funding_pipeline_graph.to_job(
    name="funding_pipeline_job",
    description="End-to-end small business funding data pipeline"
)


definitions = Definitions(
    jobs=[funding_pipeline_job],
)
