import requests
from ..config import settings

class AIPipeline:
    def __init__(self):
        self.base_url = settings.AI_SERVICE_URL

    def classify_report(self, text: str) -> str:
        """
        Classifies the report text by calling the AI Service.
        """
        try:
            payload = {"text": text, "top_k": 1}
            response = requests.post(f"{self.base_url}/api/classify", json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("category"):
                return data["category"]
            return "Unclassified"
        except Exception as e:
            print(f"Error calling AI service (classify): {e}")
            return "Unclassified"

    def summarize_reports(self, texts: list[str]) -> str:
        """
        Generates a summary from a list of report texts by calling the AI Service.
        """
        if not texts:
            return ""
            
        try:
            # Join texts for a single summary request, or use batch if supported/needed.
            # The previous implementation joined distinct reports into one text.
            # We'll stick to that logic but use the summarize endpoint.
            # Ideally, if texts are many, valid approach is to join them.
            
            combined_text = " ".join(texts)
            # Truncating client-side if needed, but service should handle or we trust it.
            # Service has a min_length 50 validation on /api/summarize request.text
            
            if len(combined_text) < 50: 
                return combined_text # Too short to summarize via AI, return as is.

            payload = {
                "text": combined_text,
                "max_length": 150,
                "min_length": 30
            }
            
            response = requests.post(f"{self.base_url}/api/summarize", json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("summary"):
                return data["summary"]
            return ""
            
        except Exception as e:
            print(f"Error calling AI service (summarize): {e}")
            return ""

ai_pipeline = AIPipeline()
