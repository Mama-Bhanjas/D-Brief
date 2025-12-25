
import requests
from typing import List, Dict
from loguru import logger

class USGSFetcher:
    """
    Level 3: The Trigger (Earthquake Sensors)
    Polls USGS for real-time seismic events in Nepal region.
    """
    URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    
    # Approx bounding box for Nepal
    LAT_MIN, LAT_MAX = 26.0, 31.0
    LON_MIN, LON_MAX = 80.0, 89.0
    
    def fetch_triggers(self) -> List[Dict]:
        try:
            response = requests.get(self.URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                features = data.get("features", [])
                
                nepal_quakes = []
                for f in features:
                    coords = f["geometry"]["coordinates"] # lon, lat, depth
                    lon, lat = coords[0], coords[1]
                    mag = f["properties"]["mag"]
                    
                    # Filter for Nepal Region + Significant Magnitude
                    if (self.LAT_MIN <= lat <= self.LAT_MAX and 
                        self.LON_MIN <= lon <= self.LON_MAX and 
                        mag >= 4.0):
                        
                        nepal_quakes.append({
                            "source": "USGS",
                            "id": f["id"],
                            "type": "Earthquake",
                            "status": "Verified sensor data",
                            "magnitude": mag,
                            "location": f["properties"]["place"],
                            "timestamp": f["properties"]["time"]
                        })
                
                if nepal_quakes:
                    logger.warning(f"USGS ALERT: Detected {len(nepal_quakes)} earthquakes in Nepal region!")
                return nepal_quakes
            return []
            
        except Exception as e:
            logger.error(f"USGS Fetch Failed: {e}")
            return []
