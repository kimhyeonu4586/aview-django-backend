import requests

from av_db import settings
from google_oauth.repository.google_oauth_repository import GoogleOauthRepository


class GoogleOauthRepositoryImpl(GoogleOauthRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.loginUrl = settings.GOOGLE['LOGIN_URL']
            cls.__instance.clientId = settings.GOOGLE['CLIENT_ID']
            cls.__instance.redirectUri = settings.GOOGLE['REDIRECT_URI']
            cls.__instance.tokenRequestUri = settings.GOOGLE['TOKEN_REQUEST_URI']
            cls.__instance.userInfoRequestUri = settings.GOOGLE['USER_INFO_REQUEST_URI']
            cls.__instance.clientSecret = settings.GOOGLE['CLIENT_SECRET']

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getOauthLink(self):
        print("getOauthLink() for Login")
        return (
            f"{self.loginUrl}?"
            f"client_id={self.clientId}&"
            f"redirect_uri={self.redirectUri}&"
            f"response_type=code&"
            f"scope=openid%20email%20profile&"
            f"access_type=offline&"
            f"prompt=consent"
        )

    def getAccessToken(self, code):
        accessToken = {
            'grant_type': 'authorization_code',
            'client_id': self.clientId,
            'redirect_uri': self.redirectUri,
            'code': code,
            'client_secret': self.clientSecret,
        }
        print(f"{accessToken}")
        response = requests.post(self.tokenRequestUri, data=accessToken)
        return response.json()

    def getUserInfo(self, accessToken):
        print("getUserInfo() 잘 들어감")
        headers = {'Authorization': f'Bearer {accessToken}'}
        print(f"{headers}")
        print(self.userInfoRequestUri)
        response = requests.get(self.userInfoRequestUri, headers=headers)
        print(f"response도 잘 들어감: {response}")
        return response.json()
