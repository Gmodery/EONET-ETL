-- Event tracks bundled to be served by the API
WITH tracks AS (
    SELECT event_id,
            struct_pack(
                event_date := event_date,
                event_coordinates := [event_longitude,event_latitude]
            ) AS coordinates,
    FROM {{ ref('mart_event_tracks_all') }}
)

SELECT event_id,
    list(coordinates) AS event_tracks
    FROM tracks
    GROUP BY event_id