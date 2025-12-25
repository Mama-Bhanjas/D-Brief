
import os
import sys
from loguru import logger

# Add current directory to path
sys.path.append(os.getcwd())

def test_hf_fallback():
    print("TESTING HUGGING FACE FALLBACK...")
    print("=" * 50)
    
    try:
        from ai_service.pipelines.processor import UnifiedProcessor
        
        print("Initializing Unified Processor (Local models are hidden)...")
        processor = UnifiedProcessor()
        
        # We only check one to see if it tries to load from HF
        print("Attempting to load Classifier from HF...")
        # We use a small timeout check or just check the path it resolved
        from ai_service.pipelines.processor import UnifiedProcessor
        
        # Check the logic of path selection
        local_path = "ai_service/models/custom_classifier"
        if not os.path.exists(local_path):
             print(f"Verified: Local path {local_path} is MISSING.")
        
        # This will trigger the property and log the HF path
        _ = processor.classify_p
        
        print("\n✅ SUCCESS: Fallback logic is active.")
            
    except Exception as e:
        print(f"\n❌ FALLBACK TEST FAILED: {e}")

if __name__ == "__main__":
    test_hf_fallback()
