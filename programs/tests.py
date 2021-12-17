from django.test     import TestCase, Client

from programs.models import Category, Program, ScreeningQuestion

class ReserveTest(TestCase):
    def setUp(self):
        client = Client()

        Program.objects.create(
            name = '테스트',
            price = 7000,
            description = '테스트프로그램 입니다.',
            address = '위코드',
            supply = '테스트 프로그램 준비물',
            limit = 3,
            start_date = '2021-12-21T16:00:00',
            running_time = 3,
        )
        ScreeningQuestion.objects.bulk_create(
            [
                ScreeningQuestion(question = '백신 접종 완료 유무를 적어주세요.', program = Program.objects.get(id = 1)),
                ScreeningQuestion(question = '본 프로그램에 대한 동의사항에 동의하시나요?', program = Program.objects.get(id = 1)),
                ScreeningQuestion(question = '', program = Program.objects.get(id = 1)),
                ScreeningQuestion(question = '백신 접종 완료 유무를 적어주세요.', program = Program.objects.get(id = 1))
            ]
        )