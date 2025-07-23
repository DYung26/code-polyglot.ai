from google.oauth2.service_account import Credentials
from googleapiclient.discovery import Resource, build

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive"
]

def get_service(service_account_file: str) -> Resource:
    creds: Credentials = Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    
    service: Resource = build("docs", "v1", credentials=creds)
    return service
