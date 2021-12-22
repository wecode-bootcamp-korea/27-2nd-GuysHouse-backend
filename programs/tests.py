import json

from django.http     import response
from django.test     import TestCase, Client

from programs.models import Program, ProgramQuestion, ScreeningQuestion, ScreeningAnswer
from users.models    import User

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
        response = self.client.get('/programs/hosting')
        mock = [{
            "program_id" : 1,
            "name" : '테스트',
            "address" : '테스트',
            "description" : '테스트',
            "thumbnail_image" : 'test.jpg'
        }]
        self.assertEqual(response.json(),{'result': mock})
        self.assertEqual(response.status_code, 200)

class ReserveTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            id = 1,
            kakao_id = '1234',
            nickname = '테스트 닉네임',
            email = 'test@test.com',
            profile_image_url = '테스트 이미지'
        )
        self.program = Program.objects.create(
            id = 1,
            name = '테스트',
            description = '테스트입니다.',
            price = 7000,
            address = 'admin',
            supply = '테스트는 필수',
            limit  = 5,
            start_date = '2021-12-21',
            running_time = 3,
            user = self.user
        )

        ScreeningQuestion.objects.bulk_create(
            [
                ScreeningQuestion(question = '테스트질문1'),
                ScreeningQuestion(question = '테스트질문2'),
                ScreeningQuestion(question = '테스트질문3'),
                ScreeningQuestion(question = '테스트질문4')
            ]
        )

        ProgramQuestion.objects.bulk_create([ProgramQuestion(program = self.program, question = question) for question in ScreeningQuestion.objects.all()])
    
    def tearDown(self):
        ScreeningQuestion.objects.all().delete()
        Program.objects.all().delete()
        User.objects.all().delete()
        ProgramQuestion.objects.all().delete()

    def test_reserve_get_success(self):
        response = self.client.get('/programs/reserve?programId=1')
        self.assertEqual(response.json(),{
            "result" : [
            {
                'question_id': 1,
                'context'    : '테스트질문1'
            },
            {
                'question_id': 2,
                'context'    : '테스트질문2'
            },
            {
                'question_id': 3,
                'context'    : '테스트질문3'
            },
            {
                'question_id': 4,
                'context'    : '테스트질문4'
            }
        ],}
        )
        self.assertEqual(response.status_code, 200)

    def test_reserve_post_success(self):
        answers = {
            'program_id' : 1,
            'question1' : '테스트1',
            'question2' : '테스트2',
            'question3' : '테스트3',
            'question4' : '테스트4'
        }
        response = self.client.post('/programs/reserve?programId=1',json.dumps(answers),content_type='application/json')
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})
        self.assertEqual(response.status_code, 201)

    def test_resrve_post_key_error(self):
        answers = {
            'program_id' : 1,
            'question1' : '테스트1',
            'question2' : '테스트2',
            'question3' : '테스트3'
        }
        response = self.client.post('/programs/reserve?programId=1',json.dumps(answers),content_type='application/json')
        self.assertEqual(response.status_code, 400)
