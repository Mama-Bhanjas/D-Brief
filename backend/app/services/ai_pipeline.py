from transformers import pipeline

class AIPipeline:
    def __init__(self):
        # Using lightweight models for demonstration
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        self.categories = ["Flood", "Earthquake", "Fire", "Storm", "Medical Emergency", "Other"]

    def classify_report(self, text: str) -> str:
        """
        Classifies the report text into one of the predefined disaster categories.
        """
        result = self.classifier(text, candidate_labels=self.categories)
        return result['labels'][0]

    def summarize_reports(self, texts: list[str]) -> str:
        """
        Generates a summary from a list of report texts.
        """
        if not texts:
            return ""
        
        combined_text = " ".join(texts)
        # Truncate to avoid token limit issues in this simple implementation
        combined_text = combined_text[:1024] 
        
        summary = self.summarizer(combined_text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

ai_pipeline = AIPipeline()
