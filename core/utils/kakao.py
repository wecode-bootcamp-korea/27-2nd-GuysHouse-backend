import json, jwt, requests

from django.http    import JsonResponse, request

class KakaoAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.user_url = 'https://kapi.kakao.com/v2/user/me'

    def get_kakao_user(self):
        try:
            headers = {"Authorization" : f'Bearer {self.access_token}'}
            result  = requests.get(self.user_url, headers=headers, timeout=3)

            if not result.status_code == 200:
                raise Exception('INVALD_USER')

            return result.json()

        except TimeoutError:
            raise Exception('TIMEOUT')