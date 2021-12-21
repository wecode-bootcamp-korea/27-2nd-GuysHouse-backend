import json, boto3, uuid

from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View
from django.db              import transaction


from programs.models        import DetailImage, Program, Category, ProgramCategory, ProgramQuestion, ScreeningAnswer, ScreeningQuestion
from users.models           import User
from programs.file_handler  import FileHanlder
from guyshouse.settings     import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET, AWS_REGION

boto3_client = boto3.client(
    's3',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

class ProgramView(View):
    @host_check_decorator
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