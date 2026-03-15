# this script is for ingesting the data into vector db after transformation
from langchain_astradb import AstraDBVectorStore
from dotenv import load_dotenv
import os 
import pandas as pd
from data_ingestion.data_transform import data_converter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
os.environ["ASTRA_DB_API_ENDPOINT"] = ASTRA_DB_API_ENDPOINT
os.environ["ASTRA_DB_APPLICATION_TOKEN"] = ASTRA_DB_APPLICATION_TOKEN
os.environ["ASTRA_DB_KEYSPACE"] = ASTRA_DB_KEYSPACE

class ingest_data:
    def __init__(self):
            
            print("data ingestion class initialized")
            self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
            self.data_converter = data_converter()
    
    def data_ingestion(self,status):    

            vstore=AstraDBVectorStore(
                  embedding=self.embeddings,
                  collection_name="Chatbotcom",
                  api_endpoint=ASTRA_DB_API_ENDPOINT,
                  token=ASTRA_DB_APPLICATION_TOKEN,
                  namespace=ASTRA_DB_KEYSPACE
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
      data_ingestion = ingest_data()
