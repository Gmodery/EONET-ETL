-- Bundled for use in API
SELECT et.event_id,
    events.timestamp_closed,
    events.event_category,
    events.event_category_id,
    et.event_tracks
FROM {{ ref('int_event_tracks_bundled') }} et
    LEFT JOIN {{ ref('stg_eonet_events') }} events USING (event_id)