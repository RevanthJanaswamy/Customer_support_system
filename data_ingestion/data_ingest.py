# script used only for reference, do not consider it as main script for data ingestion

# Disable SSL verification for httpx (used by AstraDB) to avoid certificate issues
import os
os.environ["HTTPX_INSECURE_ALLOW_ALL_HOSTS"] = "1"

# this script is for ingesting the data into vector db after transformation
from langchain_astradb import AstraDBVectorStore
from dotenv import load_dotenv
import os 
import pandas as pd
from data_ingestion.data_transform import data_converter
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

if GEMINI_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")
if ASTRA_DB_API_ENDPOINT is None:
    raise ValueError("ASTRA_DB_API_ENDPOINT environment variable is not set")
if ASTRA_DB_APPLICATION_TOKEN is None:
    raise ValueError("ASTRA_DB_APPLICATION_TOKEN environment variable is not set")
if ASTRA_DB_KEYSPACE is None:
    raise ValueError("ASTRA_DB_KEYSPACE environment variable is not set")

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
os.environ["ASTRA_DB_API_ENDPOINT"] = ASTRA_DB_API_ENDPOINT
os.environ["ASTRA_DB_APPLICATION_TOKEN"] = ASTRA_DB_APPLICATION_TOKEN
os.environ["ASTRA_DB_KEYSPACE"] = ASTRA_DB_KEYSPACE

# Disable SSL verification for httpx (used by AstraDB) to avoid certificate issues
os.environ["HTTPX_INSECURE_ALLOW_ALL_HOSTS"] = "1"

#GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "textembedding-gecko-001")

class ingest_data:
    def __init__(self):
            
            print("data ingestion class initialized")
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            self.data_converter = data_converter()
    
    def data_ingestion(self,status="Null"):    

            vstore=AstraDBVectorStore(
                  embedding=self.embeddings,
                  collection_name="Chatbotcom",
                  api_endpoint=ASTRA_DB_API_ENDPOINT,
                  token=ASTRA_DB_APPLICATION_TOKEN,
                  namespace=ASTRA_DB_KEYSPACE,
                  batch_size=10  # Process in batches of 10 to avoid quota limits
            )
            storage=status #makes sure data is stored only once in db, again and again we will not store 

            if storage==None:
                   docs=self.data_converter.data_transformation()
                   inserted_ids= vstore.add_documents(docs)
                   print(inserted_ids)
            else:
                return vstore
            
            return vstore, inserted_ids # returns them first time
                  
                
                
                
if __name__ == "__main__":
      ingest_data = ingest_data()
      vstore=ingest_data.data_ingestion("Not none") # we write none because we want to store data for the first time, none means data is not yet stored
                                         #after that we will pass the status as "stored" to avoid storing data again and again in db
      #print(f'Inserted {len(inserted_ids)} documents') 
      
      results = vstore.similarity_search("Can you tell me the low budget headphone?")

      for res in results:
        
        print(f"{res.page_content}{res.metadata}")
