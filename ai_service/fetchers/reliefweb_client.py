
import requests
from typing import List, Dict
import datetime
from loguru import logger

class ReliefWebFetcher:
    """
    Level 2: The Context (NGO Situational Reports)
    Fetches SitReps for aids and gaps.
    """
    BASE_URL = "https://api.reliefweb.int/v1/reports"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        
    def fetch_nepal_reports(self) -> List[Dict]:
        """
        Fetch specialized situation reports for Nepal.
        """
        # ReliefWeb recommends identifying your app
        headers = {
            "User-Agent": "MamaBhanjas-DisasterAI/1.0 (hackfest-project)",
            "Accept": "application/json"
        }

        payload = {
            "appname": "mama-bhanjas-hackfest",
            "profile": "list",
            "preset": "latest",
            "limit": 10,
            "filter": {
                "operator": "AND",
                "conditions": [
                    {"field": "country.name", "value": "Nepal"},
                    {"field": "format.name", "value": "Situation Report"}
                ]
            },
            "fields": {
                "include": ["title", "body", "date", "source", "url"]
            }
        }
        
        try:
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                data_list = data.get("data", [])
                logger.info(f"ReliefWeb: Fetched {len(data_list)} reports")
                return self._normalize(data_list)
            else:
                logger.error(f"ReliefWeb API Error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"ReliefWeb Fetch Failed: {e}")
            return []
            
    def _normalize(self, raw_data: List[Dict]) -> List[Dict]:
        clean_data = []
        for item in raw_data:
            fields = item.get("fields", {})
            clean_data.append({
                "source": "ReliefWeb",
                "id": str(item.get("id")),
                "type": "Context",
                "status": "Verified", # NGO reports are trusted
                "timestamp": fields.get("date", {}).get("created"),
                "title": fields.get("title"),
                "url": fields.get("url")
            })
        return clean_data
