-- Gets the latest events and their point geometries

WITH ordered_events AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY event_id
            ORDER BY event_date DESC
        ) AS rn
    FROM {{ ref('stg_eonet_geometries') }}
),
most_recent_event_dates AS (
    SELECT *
    FROM ordered_events
    WHERE rn = 1
)
SELECT event_dates.event_id,
    event_title,
    event_description,
    event_category,
    event_magnitudeUnit,
    event_magnitudeValue,
    event_date,
    event_longitude,
    event_latitude,
    timestamp_closed
FROM most_recent_event_dates AS event_dates
    LEFT JOIN (
        SELECT event_id,
            event_title,
            event_description,
            event_category,
            timestamp_closed
        FROM {{ ref('stg_eonet_events') }}
    ) AS event_details ON event_dates.event_id = event_details.event_id