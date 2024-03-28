from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def download_image(image_url, output_path):
    # Load OAuth 2.0 credentials
    credentials = Credentials.from_authorized_user_file('token.json')  # Update with your credentials file path
    print(credentials)
    # Build the Drive API service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Split the URL to get the file ID
    file_id = image_url.split('/')[-2]

    try:
        # Retrieve file metadata
        file_metadata = drive_service.files().get(fileId=file_id).execute()

        # Download the file
        request = drive_service.files().get_media(fileId=file_id)
        with open(output_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

        print(f"Image downloaded successfully to: {output_path}")

    except Exception as e:
        print(f"Error downloading image: {e}")


if __name__ == "__main__":
    image_url = 'https://drive.google.com/open?id=1nbkyHKzTyCVFLlBac0VIhcbiF9u6B7w1'
    output_path = '/Users/akashmaiti/PycharmProjects/crescendo/crescendo'
    download_image(image_url, output_path)