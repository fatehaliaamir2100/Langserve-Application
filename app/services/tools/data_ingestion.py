import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
import random

class DataIngestor:
    def __init__(self, model="text-embedding-3-small", dimensions=1536):

        self.model = model
        self.dimensions = dimensions

        openai_api_key = os.getenv("OPENAI_API_KEY")
        pinecone_api_key = os.getenv("PINECONE_API_KEY")

        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["PINECONE_API_KEY"] = pinecone_api_key
        
        self.embedding_model = OpenAIEmbeddings(model=self.model, dimensions=self.dimensions)
        self.pinecone = Pinecone(api_key=pinecone_api_key)

    def ingest_data(self, data, index_name):
        index = self.pinecone.Index(index_name)

        docs = data
        # Splitting data into smaller chunks
        
        # Embedding documents
        embeddings = self.embedding_model.embed_documents(docs)

        # Preparing documents for upsert
        documents = []
        for i, embedding in enumerate(embeddings):
            documents.append({
                "id": f"doc_{i}_{random.randint(1, 100)}",
                "values": embedding,
                "metadata": {
                    "text": docs[i]
                },
            })

        # Upserting documents to the Pinecone index
        index.upsert(documents)
      
    def retrieve_documents(self, query, index_name):
        vectorstore = PineconeVectorStore(index_name=index_name, embedding=self.embedding_model)
        return vectorstore.similarity_search(query)

ingestor = DataIngestor()

def main():
    # Example usage
    data = ["Hello!", "My name is Fateh", "The apple is blue", ]
    index_name = "bae360"
    
    # Ingest data into the Pinecone index
    ingestor.ingest_data(data, index_name)

if __name__ == "__main__":
    main()