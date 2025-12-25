
import requests
from typing import List, Dict, Optional
import datetime
from loguru import logger

class BIPADFetcher:
    """
    Level 1: The Anchor (Official Government Data)
    Fetches official incident reports from BIPAD portal.
    """
    BASE_URL = "https://bipadportal.gov.np/api/v1/incident/"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        
    def fetch_recent_incidents(self, days: int = 2) -> List[Dict]:
        """
        Fetch confirmed incidents from the last N days.
        """
        params = {
            "ordering": "-created_on",
            "limit": 50,
            # We would typically filter by date here if API supports it,
            # otherwise filter client-side.
        }
        
        try:
            # Note: This is an example call. Actual BIPAD API might require auth or exact params.
            # Assuming public access or using a placeholder if auth needed.
            response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                logger.info(f"BIPAD: Fetched {len(results)} official incidents")
                return self._normalize(results)
            else:
                logger.error(f"BIPAD API Error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"BIPAD Fetch Failed: {e}")
            return []

    def _normalize(self, raw_data: List[Dict]) -> List[Dict]:
        """Convert raw API data to our standard Verification Schema"""
        clean_data = []
        for item in raw_data:
            clean_data.append({
                "source": "BIPAD",
                "id": str(item.get("id")),
                "type": item.get("incident_type", {}).get("name", "Unknown"),
                "location": item.get("district", "Unknown"), # Simplified
                "status": "Verified",
                "timestamp": item.get("created_on"),
                "title": item.get("title", f"Incident in {item.get('district')}")
            })
        return clean_data
