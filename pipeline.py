import asyncio
from dagster import asset, Definitions, ScheduleDefinition, define_asset_job
from dagster_dbt import DbtCliResource, dbt_assets
from pathlib import Path
import subprocess

# Import your existing scripts as functions
from scraper import main as scrape_telegram_data
from enrich_images import enrich_images_with_yolo
from load_to_postgres import load_data as load_raw_to_postgres

# --- dbt Asset Definition ---

# Point to your dbt project and profiles directory
dbt_project_dir = Path(__file__).parent / "analytics"
dbt_profiles_dir = Path(__file__).parent / "dbt_profiles"

# Define the dbt resource
dbt = DbtCliResource(project_dir=str(dbt_project_dir),
                     profiles_dir=str(dbt_profiles_dir))

# This special function tells Dagster about all the models in your dbt project


@dbt_assets(manifest=dbt_project_dir / "target" / "manifest.json")
def all_dbt_models(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

# --- Python Script Asset Definitions ---

# Asset for raw scraped data


@asset
def raw_telegram_data():
    """Scrapes raw data from Telegram channels."""
    # Dagster can run async functions
    asyncio.run(scrape_telegram_data())

# Asset for enriched image data. It depends on the raw data being scraped first.


@asset(deps=[raw_telegram_data])
def enriched_yolo_data():
    """Runs YOLOv8 object detection on scraped images."""
    enrich_images_with_yolo()

# Asset for the raw tables in PostgreSQL. Depends on both scraping and enrichment.


@asset(deps=[raw_telegram_data, enriched_yolo_data])
def raw_postgres_tables():
    """Loads raw and enriched data into PostgreSQL."""
    load_raw_to_postgres()

# --- Job and Schedule Definitions ---


# Define a job that materializes all assets
all_assets_job = define_asset_job("all_assets_job", selection="*")

# Define a schedule to run the job daily
daily_schedule = ScheduleDefinition(
    job=all_assets_job,
    cron_schedule="0 0 * * *",  # Runs at midnight every day
    execution_timezone="Africa/Addis_Ababa",
)

# --- Final Definitions ---

# This is the entry point for Dagster
defs = Definitions(
    assets=[raw_telegram_data, enriched_yolo_data,
            raw_postgres_tables, all_dbt_models],
    schedules=[daily_schedule],
    resources={"dbt": dbt}
)
