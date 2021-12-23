import json, uuid, datetime, boto3

from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View
from django.db              import transaction

from django.db.models       import Q

from programs.models        import DetailImage, Program, Category, ProgramCategory, ProgramQuestion, ScreeningAnswer, ScreeningQuestion, QuestionAnswer
from users.models           import User
from core.utils.decorator   import signin_decorator, host_decorator
from programs.file_handler  import FileHanlder
from guyshouse.settings     import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET, AWS_REGION

boto3_client = boto3.client(
    's3',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

class ProgramView(View):
    @signin_decorator
    @host_decorator
    def post(self, request):
        try:
            file_hanlder    = FileHanlder(boto3_client, AWS_STORAGE_BUCKET, AWS_REGION)
            postdata        = request.POST
            thumbnail_image = request.FILES.__getitem__('thumbnail_image')
            images          = request.FILES.getlist('detail_image')
            category_ids    = Category.objects.filter(id__in = json.loads(request.POST["categoryIds"]))
            
            with transaction.atomic():
                program = Program.objects.create(
                    name                = postdata['name'],
                    description         = postdata['description'],
                    address             = postdata['address'],
                    supply              = postdata['supply'],
                    price               = postdata['price'],
                    limit               = postdata['limit'],
                    thumbnail_image_url = file_hanlder.upload_file(thumbnail_image),
                    start_date          = postdata['start_date'],
                    running_time        = postdata['running_time'],
                    user                = request.user
                )

                image_urls = file_hanlder.upload_files(images)
                
                DetailImage.objects.bulk_create([DetailImage(program = program, image_url = image_url)for image_url in image_urls])
                ProgramCategory.objects.bulk_create([ProgramCategory(program = program, category = category_id) for category_id in category_ids])
                ProgramQuestion.objects.bulk_create([ProgramQuestion(program = program, question = question) for question in ScreeningQuestion.objects.all()])

            return JsonResponse({"message":"SUCCESS"},status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)

        except transaction.TransactionManagementError:
            return JsonResponse({"message":"KEY_ERROR"},status=400)
    
    @signin_decorator
    @host_decorator
    def get(self, request):
        user     = request.user
        offset   = request.GET.get('offset', 0)
        limit    = request.GET.get('limit', 100)
        programs = Program.objects.filter(user = user)[offset:offset+limit]
        results = {
            'programs' : [{
                'program_id'     : program.id,
                'name'           : program.name,
                'description'    : program.description,
                'address'        : program.address,
                'thumbnail_image': program.thumbnail_image_url
            }for program in programs],
            'host' : {
                'nickname' : user.nickname,
                'email' : user.email,
                'profile_image' : user.profile_image_url,
                'host_description' : user.host_description
            }
        }

        return JsonResponse({'result' : results}, status = 200)

class ProgramListView(View):
    def get(self, request):
        category_id  = request.GET.getlist('category_id', None)
        is_open      = request.GET.get('is_open', None)
        sort         = request.GET.get('sort', '-created_at')
        limit        = int(request.GET.get('limit', 100))
        offset       = int(request.GET.get('offset', 0))
        
        q = Q()

        if category_id:
            q &= Q(categories__in=category_id)         
        if is_open == 'True':
            q &= Q(start_date__gte=datetime.datetime.now())
        if is_open == 'False':
            q &= Q(start_date__lt=datetime.datetime.now())

        programs = Program.objects.filter(q).order_by(sort)[offset:limit+offset]
        
        results = [{
            'id'                 : program.id,
            'name'               : program.name,
            'description'        : program.description,
            'price'              : program.price,
            'address'            : program.address,
            'start_date'         : program.start_date,
            'thumbnail_image_url': program.thumbnail_image_url,
        } for program in programs]
        
        return JsonResponse({'result' : results}, status = 200)

class ProgramDetailView(View):
    def get(self, request, program_id):
        try:
            program      = Program.objects.select_related('user').get(id=program_id)
            detail_images = DetailImage.objects.filter(program = program)
            result = {
                'id'                 : program.id,
                'name'               : program.name,
                'description'        : program.description,
                'price'              : program.price,
                'address'            : program.address,
                'start_date'         : program.start_date,
                'running_time'       : program.running_time,
                'supply'             : program.supply,
                'limit'              : program.limit,
                'thumbnail_image_url': program.thumbnail_image_url,
                'detail_image_url'   : [{'id' : detail_image.id,'image' : detail_image.image_url} for detail_image in detail_images],
                'user'               : {
                    'id'               : program.user.id,
                    'nickname'         : program.user.nickname,
                    'profile_image_url': program.user.profile_image_url,
                    'host_description ': program.user.host_description
                }
            }
            return JsonResponse({'result' : result}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except Program.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_PROGRAM'}, status = 404)

class ReserveView(View):
    @signin_decorator
    def get(self, request, program_id):
        program   = Program.objects.get(id = program_id)
        questions = ProgramQuestion.objects.select_related('question').filter(program = program)
        results   = [
            {
                'question_id': question.question.id,
                'context'    : question.question.question
            }
            for question in questions
        ]

        return JsonResponse({"result":results}, status = 200)

    @signin_decorator
    def post(self, request, program_id):
        try :
            data          = json.loads(request.body)
            user          = request.user
            program       = Program.objects.get(id = program_id)
            question_list = ScreeningQuestion.objects.filter(program = program).order_by('id')

            answers = [answer for answer in data.values()]
            answer_list = []

            for answer in answers:
                answer = ScreeningAnswer.objects.create(answer = answer, user = user)
                answer_list.append(answer)

            QuestionAnswer.objects.bulk_create(
                [
                    QuestionAnswer(
                        answer   = answer_list[question_number],
                        question = question_list[question_number]
                    ) for question_number in range(question_list.count()) 
                ]
            )

            return JsonResponse({'message':'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

        except IndexError:
            return JsonResponse({"message":"INDEX_ERROR"}, status =400)