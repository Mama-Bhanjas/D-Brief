
import requests
from typing import List, Dict
from loguru import logger
import urllib.parse

class NewsFetcher:
    """
    Level 4: The Speed (News API)
    Fetches raw news to be verified by AI.
    """
    # Using NewsData.io as discussed, standard free endpoint style
    BASE_URL = "https://newsdata.io/api/1/news"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def fetch_disaster_news(self) -> List[Dict]:
        """
        Polls for recent disaster news in Nepal.
        """
        if self.api_key == "PLACEHOLDER":
             logger.warning("NewsFetcher: No API Key provided")
             return []

        try:
            # Specific disaster keywords for Nepal to ensure strictly disaster-related news
            queries = [
                'Nepal (flood OR landslide OR earthquake OR avalanche)',
                'Nepal "forest fire" OR "wildfire"',
                'Nepal (storm OR "wind storm" OR lightning)',
                'Nepal "bridge collapse" OR "building collapse" disaster',
                'Nepal "glacial lake" outburst OR "flash flood"'
            ]
            
            # Aggregate and deduplicate
            news_results = []
            seen_links = set()
            
            for q in queries:
                params = {
                    "apikey": self.api_key,
                    "q": q,
                    "language": "en"
                }
                response = requests.get(self.BASE_URL, params=params, timeout=10)
                if response.status_code == 200:
                    for item in response.json().get("results", []):
                        link = item.get("link")
                        if link and link not in seen_links:
                            news_results.append(item)
                            seen_links.add(link)

            logger.info(f"NewsData: Found {len(news_results)} unique matching articles")
            return self._normalize(news_results)
                 
        except Exception as e:
            logger.error(f"News Fetch Failed: {e}")
            return []

    def _normalize(self, raw_data: List[Dict]) -> List[Dict]:
        clean_data = []
        for item in raw_data:
            # Combine all available text fields for better AI context
            title = item.get("title", "")
            description = item.get("description", "")
            content = item.get("content", "")
            
            full_text = f"{title}. {description}. {content}"
            
            clean_data.append({
                "source": "NewsData.io",
                "id": item.get("article_id") or item.get("link"),
                "type": "News Report",
                "status": "Unverified", 
                "timestamp": item.get("pubDate"),
                "title": title,
                "text": full_text[:2000], # Cap at 2k chars for model context
                "url": item.get("link"),
                "source_id": item.get("source_id"),
                "image_url": item.get("image_url")
            })
        return clean_data
