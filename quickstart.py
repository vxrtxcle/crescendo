import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file credentialsold3.json.
SCOPES = ["https://www.googleapis.com/auth/documents.readonly", "https://www.googleapis.com/auth/drive.metadata.readonly"]

# The ID of a sample document.
DOCUMENT_ID = "17PC0VvaCUWefxoZ8kpVjvSo406qnR8vhAFD1-1rMqEA"


def main():
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file credentialsold3.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token2.json"):
    creds = Credentials.from_authorized_user_file("token2.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token2.json", "w") as token:
      token.write(creds.to_json())

  try:
    from googleapiclient.discovery import build
    from PIL import Image
    import io

    # Create a Google Drive service object
    drive_service = build('drive', 'v3')

    # Get the image file ID
    file_id = '0APit0ZeXxgrTUk9PVA'

    # Get the image data
    image_data = drive_service.files().get_media(fileId=file_id).execute()

    # Display the image
    image = Image.open(io.BytesIO(image_data))
    image.show()


  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()

