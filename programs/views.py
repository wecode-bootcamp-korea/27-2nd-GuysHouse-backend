import json, boto3, uuid

from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View

from programs.models        import DetailImage, Program, Category, ProgramCategory, ScreeningAnswer, ScreeningQuestion
from users.models           import User
from guyshouse.settings     import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_REGION

def s3_auth():
    s3 = boto3.client(
                's3',
    	        aws_access_key_id     = AWS_ACCESS_KEY_ID,
    	        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
            )
    return s3

def put_objects(s3,image):
    unique_key = str(uuid.uuid4())
    s3.put_object(
                Bucket      = AWS_STORAGE_BUCKET_NAME,
                Key         = unique_key,
                Body        = image.file.read(),
                ContentType = image.content_type
            )
    return unique_key

class ProgramView(View):
    @host_check_decorator
    def post(self, request):
        try:
            s3              = s3_auth()
            thumbnail_image = request.FILES.__getitem__('thumbnail_image')
            detail_images   = request.FILES.getlist('detail_image')
            postdata        = request.POST

            unique_key = put_objects(s3,thumbnail_image)
            
            category_list = Category.objects.filter(name__in = postdata['categories'])

            program = Program.objects.create(
                name                = postdata['name'],
                description         = postdata['description'],
                address             = postdata['address'],
                supply              = postdata['supply'],
                price               = postdata['price'],
                limit               = postdata['limit'],
                thumbnail_image_url = '%s.s3.%s.amazonaws.com/%s' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION, unique_key),
                start_date          = postdata['start_date'],
                running_time        = postdata['running_time'],
                user                = request.user
            )
            
            for detail_image in detail_images:
                unique_key = put_objects(s3, detail_image)
                DetailImage.objects.create(
                    image_url = '%s.s3.%s.amazonaws.com/%s' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION, unique_key),
                    program   = program
                    )
            
            ProgramCategory.objects.bulk_create([ProgramCategory(program=program,category=category) for category in category_list])

            return JsonResponse({"MESSAGE":"SUCCESS"},status=201)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"},status=400)