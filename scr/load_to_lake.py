import pandas as pd
from api_connect import api_connect
from azure.storage.blob import BlobServiceClient
import os

def raw_file_to_data_lake(data):

  data_df = pd.DataFrame(data)

   # save file locally
  data_df.to_csv("civic_logic.csv", index=False)

  # Define your Azure Blob Storage account details
  ACCOUNT_KEY = os.getenv('ACCOUNT_KEY')
  container_name = 'bronze'
  blob_name = 'civic_logic_requests.csv'
  ACCOUNT_NAME = "civicpulse22"


  # Convert your pandas dataframe to a CSV string
  csv = data_df.to_csv(index=False)

  blob_service_client = BlobServiceClient(
            account_url=f"https://{ACCOUNT_NAME}.blob.core.windows.net",
            credential=ACCOUNT_KEY
        )
       
  # Upload the bytes object to Azure Blob Storage
  blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
  blob_client.upload_blob(csv, overwrite=True)
  print('upload to storage account successful')



api_response = api_connect()

raw_file_to_data_lake(api_response)