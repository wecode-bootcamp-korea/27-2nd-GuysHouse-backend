import json, os, jwt, requests

from django.views   import View
from django.http    import JsonResponse, response
from django.conf    import settings

from .models              import User
from core.utils.kakao     import KakaoAPI
from core.utils.decorator import signin_decorator
from guyshouse.settings   import SECRET_KEY, ALGORITHM

class KakaoSigninView(View):
    def get(self, request):
        try:
            access_token = request.headers['Authorization']
            kakao_api    = KakaoAPI(access_token)
            kakao_user   = kakao_api.get_kakao_user()

            user, created = User.objects.get_or_create(
                kakao_id  = kakao_user["id"],
                defaults  = {
                    'email'             : kakao_user['kakao_account']['email'],
                    'nickname'          : kakao_user['kakao_account']['profile']['nickname'],
                    'profile_image_url' : kakao_user['kakao_account']['profile']['profile_image_url'],
                }
            )

            token = jwt.encode({'id': user.id}, SECRET_KEY , ALGORITHM)

            return JsonResponse({'access_token' : token, 'is_host' : user.is_host}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class HostView(View):
    @signin_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body)
            user = request.user

            user.is_host          = True
            user.host_description = data['host_description']

            user.save()

            return JsonResponse({'is_host' : user.is_host}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)