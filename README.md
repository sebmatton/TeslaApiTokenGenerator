# Tesla API Token Generator

Tesla API Token Generator is a simple command-line tool that facilitates the generation of Tesla API tokens using Tesla's Single Sign-On (SSO) service.

## System configuration
The follow are assumed to be setup and installed to run the script:
- Python (v3)
- The following library (non-standard):
    - requests

## How to Run

To use this script, follow these steps:

1. Run the script without any parameters.
2. You will be prompted to enter your email address to initiate the login process.
3. Authenticate on Tesla's services using the dynamically generated URL.
4. After authentication, the services will redirect to a "Page not found" response.
5. At this point, copy and paste the final URL from the service back into the script.
6. The script will then generate your API token.

**Important**: This script uses random challenge values during the process. It does not use pre-defined values, ensuring that no data is transmitted to any third party. Your privacy and security are maintained throughout the token generation process.

Feel free to use this tool to obtain your Tesla API token securely.
