-- Stages eonet event information. Selects title, description, link, date closed, category, and source from raw data

WITH source AS (
    SELECT *
    FROM eonet_raw
),
event_information AS (
    SELECT id AS event_id,
        title AS event_title,
        description AS event_description,
        link AS event_link,
        closed::timestamp AS timestamp_closed,
        categories [1].id AS event_category_id,
        categories [1].title AS event_category,
        sources [1].id AS event_source,
        sources [1].url AS event_source_link,
        FROM source
)
SELECT *
FROM event_information