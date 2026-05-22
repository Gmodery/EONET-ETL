from datetime import datetime
import requests

class eonet_api:
    def __init__(self):
        self.params = {}

    def category_query(self):
        return requests.get("https://eonet.gsfc.nasa.gov/api/v3/categories").json()

    def query(self, categories=None, status=None, limit=None, days=None, start_date=None, end_date=None, bbox=None):
        params = self.params.copy()

        try:
            if categories:
                allowed_categories = ['drought', 'dustHaze', 'earthquakes', 'floods', 'landslides', 'manmade', 'seaLakeIce', 'severeStorms', 'snow', 
                         'tempExtremes', 'volcanoes', 'waterColor', 'wildfires', 'Drought', 'Dust and Haze', 'Earthquakes', 'Floods', 
                         'Landslides', 'Manmade', 'Sea and Lake Ice', 'Severe Storms', 'Snow', 'Temperature Extremes', 'Volcanoes', 'Water Color', 'Wildfires']
                cats = ""
                
                if type(categories) is list:
                    for category in categories:
                        if category not in allowed_categories:
                            raise ValueError(f"Category {category} not allowed. Must be one of {allowed_categories}")

                        cats += category
                        cats += ','

                elif type(categories) is str:
                    if categories.lower() == 'all':
                        for category in allowed_categories[:13]:
                            cats += category
                            cats += ','
                        
                    else:
                        cats += categories

                else:
                    raise ValueError("Invalid category type. Must be either list or str")
                
                params['category'] = cats

            
            if status:
                if type(status) is str and status.lower() in ['open', 'closed', 'all']:
                    params['status'] = status

                else:
                    raise ValueError("Status not in ['open', 'closed', 'all']")
                

            if limit:
                if type(limit) is int:
                    params['limit'] = limit

                else:
                    raise ValueError("Limit must be integer")
                

            if days:
                if type(days) is int:
                    params['days'] = days

                else:
                    raise ValueError("Days must be integer")
                

            if start_date and end_date:
                try:
                    datetime.strptime(start_date, "%Y-%m-%d")

                    params["start"] = start_date

                    datetime.strptime(end_date, "%Y-%m-%d")
                    params["end"] = end_date
                
                except ValueError:
                    raise ValueError("Date formatted incorrectly. Must be of form YYYY-MM-DD")
                
            elif start_date is None and end_date is None:
                pass

            else:
                raise ValueError("Start and End date must be provided")
            


            if bbox:
                if type(bbox) is tuple:
                    min_lon, max_lat, max_lon, min_lat = bbox

                    params['bbox'] = f"{min_lon},{max_lat},{max_lon},{min_lat}"

                else:
                    raise ValueError("bbox must be a tuple of form (min_lon, max_lat, max_lon, min_lat)")



        
        except ValueError as ve:
            raise ValueError(ve)

                
        
        return requests.get(f"https://eonet.gsfc.nasa.gov/api/v3/events?", params=params).json()
    