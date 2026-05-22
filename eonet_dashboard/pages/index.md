---
title: NASA EONET Observation Data
neverShowQueries: true
---

# Data Overview
## Source
NASA's Earth Observatory Natural Event Tracker [EONET](https://eonet.gsfc.nasa.gov) provides a curated reference of continuously updated natural event metadata in near-real time. 


## Open and Closed Events
Certain events are considered closed when they have completed unfolding. For instance, for wildfires this would mean full containment. By contrast, open events are still ongoing. Any "active" events are considered as such by the available EONET data.


## Data Range
Currently active events begin as early as <Value data={min_date_active}/>
with the most recent observation being on <Value data={max_date_active}/>

```sql min_date_active
SELECT min(event_date) FROM mart_event_tracks_active
```

```sql max_date_active
SELECT max(event_date) FROM mart_event_tracks_active
```




# Active Events
## Open Event Observations
The most recent observations for events that have yet to be closed.

```sql active_events
  SELECT 
    event_title AS Event,
    event_description AS description,
    event_category AS Category,
    event_magnitudeValue AS Magnitude,
    event_magnitudeUnit AS Unit,
    event_date AS "Latest Observation",
    event_latitude,
    event_longitude
  FROM mart_latest_open_observations
  ORDER BY "Latest Observation" DESC
```

<DataTable data={active_events}/>



## Currently Active Events by Category
```sql events_by_category
  SELECT 
    event_category AS Category,
    count(distinct(event_id)) AS "Total Active Instances"
  FROM mart_latest_open_observations
  GROUP BY Category
```

<DataTable data={events_by_category}/>

<BarChart
    data="{events_by_category}"
    x=Category
    y="Total Active Instances"
/>


## Active Event Locations
<PointMap 
    data={active_events} 
    lat=event_latitude 
    long=event_longitude 
    value=Category
    pointName=Event
    height=300
/>


# Event Trends
## Event Trends Over The Past Year
```sql event_trends
  SELECT *
  FROM mart_events_by_category
  WHERE week > today() - INTERVAL 1 YEAR
  ORDER BY week ASC
```

<LineChart
data={event_trends}
x=week
y=count
series=event_category
xAxisTitle="Month"
yAxisTitle="Number of Instances"
subtitle="Number of Event Instances"
/>


<LineChart
data={event_trends}
x=week
y=avg_magnitude
series=event_category
xAxisTitle="Month"
yAxisTitle="Average Magnitude"
subtitle="Number of Event Instances"
/>



