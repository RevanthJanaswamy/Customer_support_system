import pandas as pd
from langchain_core.documents import Document

class data_converter:

    def __init__(self):
         print("data transformation started")
         self.product_data = pd.read_csv("data\\flipkart_product_review.csv")
         #print(self.product_data.head())


    def data_transformation(self):
        required_columns = self.product_data.columns
        required_columns=list(required_columns[1:])
        #print(required_columns)

        product_list=[]

        for index, row in self.product_data.iterrows(): #The iterrows() method in pandas generates an iterator object of the DataFrame, 
                                                        #allowing us to iterate each row in the DataFrame

            object = {

                "product_name": row['product_title'],
                "product_rating":row['rating'],
                "product_review":row['review'], 
                "summary": row['summary']
            }
            product_list.append(object)
        # print("****below is my product list*****")
        # print(product_list[0])

        documnts = []

        for entry in product_list:

            metadata = {"product_name": entry['product_name'], "product_rating": entry['product_rating'],
            "product_summary": entry['summary'] }
            #the Document object should be stored in vector db
            doc = Document(page_content=entry['product_review'], metadata=metadata) 
            documnts.append(doc)
        print(documnts[0])



    
    
if __name__ == "__main__":
    data_con = data_converter()
    data_con.data_transformation()
