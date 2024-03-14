from urllib.parse import urlencode

# Client ID obtained from the Google Cloud Console
client_id = "996300235376-o8uavv21pvhngkqpf863gbpp9vsl1r93.apps.googleusercontent.com"

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
# https://crescendofrc2468.streamlit.app/Pit_Scouting?code=4/0AeaYSHCqsmGkIgFYgtKJuqD4VEZQtdgf6X3F3tQavTibLOfm0eTHeLAL0HcBVIbVBDIhfw&scope=https://www.googleapis.com/auth/drive
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

# Extract the access token and refresh token from the response
access_token = token_data['access_token']
refresh_token = token_data['refresh_token']
'''
# Now you can use the access token and refresh token as needed

