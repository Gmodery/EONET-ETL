-- Stages eonet event geometries. Some events such as storms have multiple geometries,
-- so these are kept separate from event information

WITH source AS (
    SELECT *
    FROM eonet_raw
),
event_geometry AS (
    SELECT id AS event_id,
        unnest(geometry, recursive := true) AS geometry
    FROM source
)
SELECT event_id,
    magnitudeUnit AS event_magnitudeUnit,
    magnitudeValue AS event_magnitudeValue,
    date::timestamp AS event_date,
    type AS geo_type,
    coordinates [1] AS event_longitude,
    coordinates [2] AS event_latitude
FROM event_geometry