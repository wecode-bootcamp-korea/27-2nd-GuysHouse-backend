from django.urls import path

from .views import KakaoSigninView, HostView

urlpatterns = [
    path('/kakao/signin' , KakaoSigninView.as_view()),
    path('/host', HostView.as_view()),
]