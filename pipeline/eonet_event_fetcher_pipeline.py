import subprocess, os
from eonet_fetcher import fetch_and_store_eonet_data
from prefect import task, flow
from datetime import timedelta


# Fetch task
@task(retries=2, retry_delay_seconds=5, log_prints=True)
def fetch_and_store():
    print("Running fetch and store flow")
    n_records = fetch_and_store_eonet_data()
    print(f"Completed fetch and store flow \nTotal records: {n_records}")

    
# dbt execution task
@task(log_prints=True)
def run_dbt_build():
    dbt_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "eonet_dbt")

    print("Starting dbt build")
    
    result = subprocess.run(
        ["dbt", "build", "--project-dir", dbt_dir],
        capture_output=True, text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        raise Exception(f"dbt build failed: \n{result.stderr}")



# Flow
@flow(name="eonet_pipeline")
def eonet_pipeline():
    fetch_and_store_eonet_data()
    run_dbt_build()



if __name__ == "__main__":
    eonet_pipeline.serve(
        name="eonet_scheduled_run",
        interval=timedelta(hours=6)
    )