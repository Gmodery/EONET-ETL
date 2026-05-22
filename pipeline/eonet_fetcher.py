import pandas as pd
import duckdb, os
from eonet_api import eonet_api
from prefect import flow, task

@task(retries=3, retry_delay_seconds=7)
def fetch_category_data():
    api = eonet_api()

    response = api.category_query()

    try:
        response["categories"]
    except KeyError:
        raise KeyError("API Rate limited")

    return response

@task(retries=3, retry_delay_seconds=7)
def fetch_eonet_data(categories, status, days):
    api = eonet_api()

    response = api.query(categories=categories, status=status, days=days)

    try:
        response["events"]
    except KeyError:
        raise KeyError("API Rate limited")

    return response

@task
def expand_json_to_df(response, expansion_column):
    df = pd.DataFrame(response[expansion_column])

    return df

@task
def store_event_data(df):
    con = duckdb.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data\\eonet_data.db"))

    try:
        con.sql("CREATE TABLE IF NOT EXISTS eonet_raw AS SELECT * FROM df")
        con.sql("ALTER TABLE eonet_raw ADD PRIMARY KEY (id)")

    except duckdb.CatalogException:
        # Table already made
        pass


    con.sql("""
            INSERT INTO eonet_raw SELECT * FROM df
            ON CONFLICT (id) DO UPDATE SET id = EXCLUDED.id
            """)

    con.close()

    return 1



@task
def store_category_data(df):
    con = duckdb.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data\\eonet_data.db"))

    try:
        con.sql("CREATE TABLE category_raw AS SELECT * FROM df")
        con.sql("ALTER TABLE category_raw ADD PRIMARY KEY (id)")

    except duckdb.CatalogException:
        # Table already made
        pass


    con.sql("""
            INSERT INTO category_raw SELECT * FROM df
            ON CONFLICT (id) DO UPDATE SET id = EXCLUDED.id
            """)

    con.close()

    return 1


@flow
def fetch_and_store_eonet_data(categories='all', status='all', days=365):
    event_api_data = fetch_eonet_data(categories, status, days)
    cat_api_data = fetch_category_data()

    event_data = expand_json_to_df(event_api_data, 'events')
    cat_data = expand_json_to_df(cat_api_data, 'categories')


    store_event_data(event_data)
    store_category_data(cat_data)

    con = duckdb.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data\\eonet_data.db"))

    count = con.execute("SELECT count(*) FROM eonet_raw").fetchone()[0]

    con.close()

    return count


if __name__ == "__main__":
    fetch_and_store_eonet_data()