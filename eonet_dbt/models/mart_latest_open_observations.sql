-- Gets latest observations that are still open

SELECT *
FROM {{ ref('int_latest_observation') }}
WHERE timestamp_closed is NULL