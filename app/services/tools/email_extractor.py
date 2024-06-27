import os
from dotenv import load_dotenv
import requests
from msal import ConfidentialClientApplication
from app.services.tools.data_ingestion import ingestor

# Azure AD app registration details
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
SCOPE = [os.getenv('SCOPE')]

# Function to get an access token from Azure AD
def get_access_token():
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET,
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not obtain access token")

# Function to get emails from Microsoft 365
def get_emails_from_microsoft_365(query: str) -> list:
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://graph.microsoft.com/v1.0/me/messages"

    # Optionally, include query parameters to filter or search emails
    params = {
        "$search": query,
        "$top": 10  # Limit the number of results
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    emails = response.json().get('value', [])
    return emails

# Main function to run the script manually
def get_emails(query: str, index: str) -> list:
    try:
        emails = get_emails_from_microsoft_365(query)
        ingestor.ingest_data(emails, index)
        return emails
    except requests.exceptions.RequestException as e:
        print(f"Error fetching emails: {e}")
        return []

if __name__ == "__main__":
    query = input("Enter the query to search emails: ")
    index = input("Enter the index: ")
    emails = get_emails(query, index)
    print(emails)
