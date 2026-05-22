import duckdb, os
import pandas as pd
from fastapi import FastAPI

app = FastAPI(title="EONET API")

def db_connect():
    return duckdb.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", "eonet_data.db"))


def status_category_querybuilder(query, status=None, category=None):
    if category or status:
        query += " WHERE "
        prev = False

        if category:
            # Separate out list of items
            categories = category.split(',')

            # Merge back into lowered string
            cat_query_str = ""
            for cat in categories:
                cat_query_str += f"'{cat.lower()}',"

            cat_query_str = cat_query_str[:-1]

            query += f"lower(event_category_id) IN ({cat_query_str})"
            
            prev = True


        if status and status != 'all':
            if prev:
                query += " AND  "

            if status == "open":
                query += "timestamp_closed IS NULL"

            elif status == "closed":
                query += "timestamp_closed IS NOT NULL"

    return query



@app.get("/categories")
def get_categories():
    con = db_connect()

    res = con.execute("SELECT * FROM stg_category_info").df()

    con.close()

    return res.to_dict(orient="records")



@app.get("/events/tracks")
def get_event_tracks(category: str = None, status: str = None):
    con = db_connect()
    
    query = "SELECT * FROM mart_event_tracks_bundled"

    query = status_category_querybuilder(query, status=status, category=category)

    cursor = con.execute(query)

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    res = [dict(zip(columns, row)) for row in rows]

    con.close()

    return res



@app.get("/events/{event_id}/tracks")
def get_event_tracks(event_id: str):
    print("here")
    con = db_connect()
    
    query = "SELECT * FROM mart_event_tracks_bundled WHERE event_id = ?"

    cursor = con.execute(query, [event_id])

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    res = [dict(zip(columns, row)) for row in rows]

    con.close()

    return res



@app.get("/events/{event_id}")
def get_event_info(event_id: str):
    con = db_connect()

    res = con.execute(
        "SELECT * FROM stg_eonet_events WHERE event_id = ?",
        [event_id]
    ).df()

    con.close()

    return res.to_dict(orient="records")







@app.get("/events")
def get_event_info(category: str = None, status: str = None):
    con = db_connect()
    
    query = "SELECT * FROM stg_eonet_events"

    query = status_category_querybuilder(query, category=category, status=status)

    res = con.execute(query).df()

    con.close()

    return res.to_dict(orient="records")