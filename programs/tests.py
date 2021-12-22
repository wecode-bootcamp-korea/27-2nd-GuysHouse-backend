from django.http import response
from django.test     import TestCase, Client

from .models import Program
from users.models import User

class ProgramTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            kakao_id = '테스트',
            nickname = '테스트',
            profile_image_url = '테스트',
            email = 'test@test.com'
        )
        self.program = Program.objects.create(
            name = '테스트',
            address = '테스트',
            description = '테스트',
            supply = '테스트',
            price = 5000,
            start_date = '2021-12-22',
            running_time = 3,
            limit = 5,
            user = self.user,
            thumbnail_image_url = 'test.jpg'
        )
    
    def tearDown(self):
        User.objects.all().delete()
        Program.objects.all().delete()
    
    def test_programview_get_success(self):
        response = self.client.get('/programs')
        mock = [{
            "name" : '테스트',
            "address" : '테스트',
            "description" : '테스트',
            "thumbnail_image" : 'test.jpg'
        }]
        self.assertEqual(response.json(),{'result': mock})
        self.assertEqual(response.status_code, 200)
