from django.test   import Client, TestCase
from unittest.mock import patch, MagicMock

class SignInTest(TestCase):
    @patch("core.utils.KakaoAPI.requests")
    def test_kakao_signin_user_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id":126463,
                    "kakao_account": { 
                        "profile_needs_agreement": False,
                        "profile": {
                            "nickname": "유민혁",
                            "thumbnail_image_url": "http://yyy.kakao.com/.../img_110x110.jpg",
                            "profile_image_url": "http://yyy.kakao.com/dn/.../img_640x640.jpg",
                            "is_default_image":False
                            }
                        }
                    }
                    
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization" : "가짜 access_token"}
        response            = client.get("/users/kakao/signin", **headers)

        self.assertEqual(response.status_code, 201)