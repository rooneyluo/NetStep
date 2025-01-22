import requests

class OAuthProvider:
    @staticmethod
    def verify_google_token(token: str) -> dict:
        response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
        if response.status_code != 200:
            raise ValueError("Invalid Google token")
        return response.json()

    @staticmethod
    def verify_line_token(token: str) -> dict:
        response = requests.get(f"https://api.line.me/oauth2/v2.1/verify?access_token={token}")
        if response.status_code != 200:
            raise ValueError("Invalid LINE token")
        return response.json()
