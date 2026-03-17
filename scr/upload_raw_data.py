import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from pathlib import Path

location = Path(__file__).resolve().parent
project_root = location.parent

load_dotenv()

# 1. Configuration - Get these from your Terraform outputs or Azure Portal
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
ACCOUNT_KEY = os.getenv("ACCOUNT_KEY")
CONTAINER_NAME = "bronze"
LOCAL_FILE_PATH = project_root / "civic_logic.csv"

BLOB_NAME = "civic_logic_requests.csv"

def upload_huge_file():
    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
            credential=ACCOUNT_KEY
        )
       
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

        print(f" Starting upload: {LOCAL_FILE_PATH}...")

        with open(LOCAL_FILE_PATH, "rb") as data:
            blob_client.upload_blob(
                data,
                overwrite=True,
                # Adjust max_concurrency for even more speed 
                # (uses multiple threads to upload chunks)
                max_concurrency=4 
            )

        print(f"Upload complete! File is now in container: {CONTAINER_NAME}")

    except Exception as e:
        print(f"Failed to upload: {e}")

if __name__ == "__main__":
    upload_huge_file()