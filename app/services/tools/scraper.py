import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.tools.data_ingestion import ingestor

def get_url_data(url: str, index: str) -> list:
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from elements
        all_text = soup.get_text(separator=' ', strip=True)

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=16384, chunk_overlap=2048, length_function=len)
        docs = text_splitter.split_text(all_text)

        print(docs)
        # Ingest data
        ingestor.ingest_data(docs, index)
        return docs

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

if __name__ == "__main__":
    url = input("Enter the URL: ")
    index = input("Enter the index: ")
    get_url_data(url, index)
