-- Event geometry history, including id, title, category, observation timestamp, magnitude, and point
SELECT e.event_id,
    e.event_title,
    e.event_description,
    e.event_category,
    g.event_magnitudeUnit,
    g.event_magnitudeValue,
    g.event_date,
    g.event_longitude,
    g.event_latitude,
    e.timestamp_closed
FROM {{ ref('stg_eonet_events') }} e
    INNER JOIN {{ ref('stg_eonet_geometries') }} g on e.event_id = g.event_id
WHERE e.timestamp_closed is NULL
ORDER BY e.event_id,
    g.event_date