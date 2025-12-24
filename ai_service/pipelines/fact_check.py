"""
Fact Checking Pipeline
Verifies claims by searching the internet for corroborating sources
"""
from typing import Dict, List, Optional
import time
from loguru import logger
from duckduckgo_search import DDGS

from ai_service.utils.source_checker import SourceChecker
from ai_service.utils import TextPreprocessor

class FactCheckPipeline:
    """
    Pipeline that searches the web to verify news
    """
    
    def __init__(self):
        self.source_checker = SourceChecker()
        self.preprocessor = TextPreprocessor()
        logger.info("FactCheck pipeline initialized")
        
    def verify_claim(self, text: str) -> Dict[str, any]:
        """
        Verify a text claim by searching for it
        
        Args:
            text: The news text to verify
            
        Returns:
            Verification result with found sources
        """
        # 1. Generate Query
        clean_text = self.preprocessor.clean_text(text)
        words = clean_text.split()
        # Improve query: use first 15 words + "news" to guide search engine
        if len(words) > 15:
             query = " ".join(words[:15]) + " news"
        else:
             query = clean_text + " news"
             
        logger.info(f"Fact checking query: {query}")
        
        # 2. Search Web
        sources = []
        try:
            with DDGS(proxies=None) as ddgs:
                # Use default region to avoid empty results in restricted environments
                results = list(ddgs.text(query, max_results=8))
                
            found_trusted = False
            found_untrusted = False
            trusted_sources = []
            untrusted_sources = []
            
            for r in results:
                url = r['href']
                title = r['title']
                
                # Filter out likely irrelevant/foreign results (e.g. Baidu, Zhihu)
                if "zhihu.com" in url or "baidu.com" in url:
                    continue
                    
                source_result = self.source_checker.check_source(url)
                status = source_result["status"]
                score = source_result["source_score"]
                
                source_info = {
                    "url": url,
                    "title": title,
                    "status": status
                }
                
                if status == "Trusted":
                    found_trusted = True
                    trusted_sources.append(source_info)
                elif status == "Untrusted":
                    found_untrusted = True
                    untrusted_sources.append(source_info)
                
                sources.append(source_info)
                
            # 3. Formulate Verdict
            verification_status = "Unverified"
            confidence = 0.0
            explanation = "No relevant sources found."
            
            if found_trusted:
                verification_status = "Verified"
                confidence = 1.0
                explanation = f"Corroborated by trusted sources: {', '.join([s['title'] for s in trusted_sources[:2]])}"
            elif found_untrusted and not found_trusted:
                verification_status = "Fake"
                confidence = 0.9
                explanation = f"Found only on known untrusted sources: {', '.join([s['title'] for s in untrusted_sources[:2]])}"
            elif sources:
                # Found mixed/unknown sources
                verification_status = "Unverified"
                confidence = 0.4
                explanation = f"Found on {len(sources)} sources, but none are in our Trusted list. Manual review recommended."
            
            return {
                "success": True,
                "status": verification_status,
                "confidence": confidence,
                "is_reliable": verification_status == "Verified",
                "sources": sources,
                "explanation": explanation
            }
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "status": "Error",
                "is_reliable": False
            }
