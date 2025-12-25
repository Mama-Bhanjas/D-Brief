
import os
from huggingface_hub import HfApi, create_repo, login
from dotenv import load_dotenv

load_dotenv()

def upload_models():
    token = os.getenv("HF_TOKEN")
    if not token:
        print("❌ Error: HF_TOKEN not found in .env file.")
        print("Please get a 'Write' token from https://huggingface.co/settings/tokens and add it to .env")
        return

    login(token=token)
    api = HfApi()
    
    # Get username
    user_info = api.whoami()
    username = user_info['name']
    print(f"✅ Logged in as: {username}")

    models = {
        "classifier": "ai_service/models/custom_classifier",
        "summarizer": "ai_service/models/custom_summarizer",
        "ner": "ai_service/models/custom_ner",
        "verifier": "ai_service/models/custom_verifier"
    }

    repo_base = "nepal-disaster"
    
    for key, path in models.items():
        if not os.path.exists(path):
            print(f"⚠️ Skipping {key}: Path {path} does not exist.")
            continue
            
        repo_id = f"{username}/{repo_base}-{key}"
        print(f"\n🚀 Uploading {key} to {repo_id}...")
        
        try:
            # Create repo if not exists
            create_repo(repo_id=repo_id, exist_ok=True, repo_type="model")
            
            # Upload folder
            # We exclude checkpoints to save space/time
            api.upload_folder(
                folder_path=path,
                repo_id=repo_id,
                repo_type="model",
                ignore_patterns=["checkpoint-*", "*.bak", "*.log", "__pycache__"]
            )
            print(f"✅ Successfully uploaded {key}!")
        except Exception as e:
            print(f"❌ Failed to upload {key}: {e}")

    print("\n🎉 All uploads finished! Now you can update your code to use these IDs.")

if __name__ == "__main__":
    upload_models()
