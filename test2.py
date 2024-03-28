
'''from urllib.parse import urlencode

# Client ID obtained from the Google Cloud Console
client_id = "426561909353-lo3n92o2gk2k08ae03muajdl47jgkugh.apps.googleusercontent.com"

# Redirect URI where Google will redirect the user after granting permission
redirect_uri = "https://crescendofrc2468.streamlit.app/Pit_Scouting"

# Scopes required by your application
scopes = ["https://www.googleapis.com/auth/drive"]

# Construct the authorization URL
authorization_url = "https://accounts.google.com/o/oauth2/auth?" + urlencode({
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": " ".join(scopes),
    "response_type": "code"
})

# Redirect the user to the authorization URL
print("Visit the following URL to authorize your application:")
print(authorization_url)

# https://crescendofrc2468.streamlit.app/Pit_Scouting?code=4/0AeaYSHC4pKpQHP1Dt2_gYTWeYi3CPNhEwfK_ikT7DHqlFkTuhoaqmXj_G9U-9-Q-_9i2ow&scope=https://www.googleapis.com/auth/drive

# https://crescendofrc2468.streamlit.app/Pit_Scouting?code=4/0AeaYSHCqsmGkIgFYgtKJuqD4VEZQtdgf6X3F3tQavTibLOfm0eTHeLAL0HcBVIbVBDIhfw&scope=https://www.googleapis.com/auth/drive
# https://crescendofrc2468.streamlit.app/Pit_Scouting?code=4/0AeaYSHCThh3enzUOyJzfR_u71tYGuUkBeZXvyyCSIM0nCLeuSOhepek4Mnx6QnOBBIbkHw&scope=https://www.googleapis.com/auth/drive
'''
'''
# 4/0AeaYSHCqsmGkIgFYgtKJuqD4VEZQtdgf6X3F3tQavTibLOfm0eTHeLAL0HcBVIbVBDIhfw
import requests

# Define the token endpoint URL
token_url = "https://oauth2.googleapis.com/token"

# Define the parameters for the token exchange request
params = {
    "code": '4/0AeaYSHCqsmGkIgFYgtKJuqD4VEZQtdgf6X3F3tQavTibLOfm0eTHeLAL0HcBVIbVBDIhfw',
    "client_id": "996300235376-o8uavv21pvhngkqpf863gbpp9vsl1r93.apps.googleusercontent.com",
    "client_secret": "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",
    "redirect_uri": "https://crescendofrc2468.streamlit.app/Pit_Scouting",
    "grant_type": "authorization_code"
}

# Make the POST request to exchange the authorization code for tokens
response = requests.post(token_url, data=params)

# Parse the response JSON
token_data = response.json()
print(token_data)

# Extract the access token and refresh token from the response
access_token = token_data['access_token']
refresh_token = token_data['refresh_token']

# Now you can use the access token and refresh token as needed

'''
'''
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from PIL import Image

# Define the scopes for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def download_image(file_id, output_path):
    """
    Download an image from Google Drive and save it to the specified output path.
    """
    # Set up the credentials flow
    flow = InstalledAppFlow.from_client_secrets_file(
        'token.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Build the Drive API service
    service = build('drive', 'v3', credentials=creds)

    # Download the file
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = io.BytesIO()
    downloader.write(request.execute())
    downloader.seek(0)
    img = Image.open(downloader)
    img.save(output_path)


file_id = '1nbkyHKzTyCVFLlBac0VIhcbiF9u6B7w1'

# Specify the path where you want to save the downloaded image
output_path = 'image.jpg'

download_image(file_id, output_path)
'''
'''
import streamlit as st
from googleapiclient.discovery import build

# Specify the API key
API_KEY = 'AIzaSyC6x1jLpQLHqMxWf3CnHKq4rgGvebkSgmQ'

# Create a service object for interacting with the Picker API
service = build('picker', 'v1', developerKey=API_KEY)
import tempfile
import os
import streamlit

# Function to download image using Google Picker API
def download_image():
    # Initialize Google Picker
    picker = GooglePicker()

    # Configure Google Picker to select images from Google Drive
    picker.set_params(
        views=["DocsUploadView().setIncludeFolders(true)"],
        mime_types=["image/png", "image/jpeg"]
    )

    # Prompt user to select an image
    image_url = picker.show()

    # Download the selected image to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    os.system(f"wget -O {temp_file.name} {image_url}")

    return temp_file.name

# Main function to create Streamlit app
def main():
    st.title("Display Image from Google Drive")

    # Download the image using Google Picker API
    image_path = download_image()

    # Display the downloaded image
    st.image(image_path, caption="Downloaded Image from Google Drive")

main()
'''
'''
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import streamlit as st

# Set up Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = None

# Check if credentials file exists
if os.path.exists('credentialsold3.json'):
    creds = Credentials.from_authorized_user_file('credentialsold3.json')

# If there are no (valid) credentials available, let the user log in
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'token.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # Save credentials for the next run
    with open('credentialsold3.json', 'w') as token:
        token.write(creds.to_json())

# Initialize the Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

# Search for image files in Google Drive (you can customize the query)
response = drive_service.files().list(
    q="mimeType='image/jpeg' or mimeType='image/png'",
    fields="files(id, name)"
).execute()

# Get the first image file (you may modify this logic as needed)
image_file = response.get('files', [])[0]

# Download the image file
image_request = drive_service.files().get_media(fileId=image_file['id'])
image_content = image_request.execute()

# Display image using Streamlit
st.image(image_content, caption=image_file['name'])
'''
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import streamlit as st

# Set up Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None

# Check if credentials file exists
if os.path.exists('credentialsold3.json'):
    creds = Credentials.from_authorized_user_file('credentialsold3.json')

# If there are no (valid) credentials available, let the user log in
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentialsold3.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # Save credentials for the next run
    with open('credentialsold3.json', 'w') as token:
        token.write(creds.to_json())

# Initialize the Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

# Search for image files in Google Drive (you can customize the query)
response = drive_service.files().list(
    q="mimeType='image/jpeg' or mimeType='image/png'",
    fields="files(id, name)"
).execute()

# Get the first image file (you may modify this logic as needed)
image_file = response.get('files', [])[0]

# Download the image file
image_request = drive_service.files().get_media(fileId=image_file['id'])
image_content = image_request.execute()

# Display image using Streamlit
st.image(image_content, caption=image_file['name'])
