header = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                     TESLA API Token Generator                  ┃
┃                         Version: 1.0.0                         ┃
┃                     Author: Sébastien Matton                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

# Token generation method is documented here: https://tesla-api.timdorr.com/api-basics/authentication#step-3-exchange-authorization-code-for-bearer-token
# This script will run using random challenge values. No pre-defined values will be used, and therefore, no data will be transmitted to any third party.

import secrets
import hashlib
import base64
import string
import requests
import webbrowser
from urllib.parse import urlparse, parse_qs
import json

# Print header
print(header)

# Get user email address
login_email = input("> Enter your email address: ")

# Generate an 86-character random string
characters = string.ascii_letters + string.digits
code_verifier = ''.join(secrets.choice(characters) for x in range(86))

# Calculate the SHA-256 hash of the code_verifier
sha256 = hashlib.sha256()
sha256.update(code_verifier.encode('utf-8'))
digest = sha256.digest()

# Generate an other 15-character random string
oauth_random = ''.join(secrets.choice(characters) for x in range(15))

# Encode the SHA-256 hash using base64
code_challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode('utf-8')

# Setup the url
base_url = "https://auth.tesla.com/oauth2/v3/authorize"
params = {
    'client_id': 'ownerapi',
    'code_challenge': code_challenge,
    'code_challenge_method': 'S256',
    'redirect_uri': 'https://auth.tesla.com/void/callback',
    'response_type': 'code',
    'scope': 'openid email offline_access',
    'state': oauth_random,
    'login_hint': login_email
}
url_with_params = f"{base_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
print("\nThe following url will open in your browser: " + url_with_params)
print("\nAfter successfully authenticating your Tesla account, copy the url of the \"Page Not Found\" page (Should be in the form \"https://auth.tesla.com/void/callback?code=...\").")
input("\nType ENTER to proceed...")

# Open web browser
webbrowser.open(url_with_params)

# Retrieve final url
response_url = input("\n> Paste the url you obtained after login: ")

# Parse the URL
parsed_url = urlparse(response_url)

# Retrieve the "code" parameter
query_parameters = parse_qs(parsed_url.query)
code_parameter = query_parameters.get('code', [''])[0]

# -- STEP 3 -- 
# Define the base URL for your API endpoint
base_url = "https://auth.tesla.com/oauth2/v3/token"

# Define the parameters you want to include in the request body as a dictionary
payload = {
  "grant_type": "authorization_code",
  "client_id": "ownerapi",
  "code": code_parameter,
  "code_verifier": code_verifier,
  "redirect_uri": "https://auth.tesla.com/void/callback"
}

# Send the POST request with the parameters
response = requests.post(base_url, data=payload)

# Check the response status code and content
if response.status_code == 200:
    print("\nToken request successful!")
    response_json = json.loads(response.text)
    print("\n=> Access token: ", response_json["access_token"])
    print("\n=> Refresh token: ", response_json["refresh_token"])
else:
    print("\Token request failed with status code: ", response.status_code)

print("\n\nDone!")