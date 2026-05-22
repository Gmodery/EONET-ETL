-- Number of events by category and week
WITH event_cats AS (
    SELECT event_id,
        event_category
    FROM {{ ref('stg_eonet_events') }}
)
SELECT event_category,
    date_trunc('week', geo.event_date)::timestamp AS week,
    count(distinct ec.event_id) AS count,
    avg(geo.event_magnitudeValue) AS avg_magnitude
FROM event_cats ec
    INNER JOIN (
        SELECT event_id,
            event_date,
            event_magnitudeValue
        FROM {{ ref('stg_eonet_geometries') }}
    ) geo ON ec.event_id = geo.event_id
GROUP BY 1, 2