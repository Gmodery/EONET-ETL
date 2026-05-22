WITH source AS (
    SELECT * FROM category_raw
)

SELECT id AS category_id,
title AS category_title,
description AS category_description,
FROM source