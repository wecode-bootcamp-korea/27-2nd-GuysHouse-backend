from django.db    import models

from core.models  import TimeStampModel

class Category(models.Model): 
    name = models.CharField(max_length=300)
    
    class Meta: 
        db_table = 'categories'

class Program(TimeStampModel): 
    name                = models.CharField(max_length=300)
    description         = models.CharField(max_length=300)
    address             = models.CharField(max_length=300)
    supply              = models.CharField(max_length=300)
    price               = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    limit               = models.PositiveSmallIntegerField(default=1)
    count               = models.SmallIntegerField(default=0)
    thumbnail_image_url = models.CharField(max_length=2000)
    start_date          = models.DateTimeField()
    running_time        = models.PositiveSmallIntegerField()
    user                = models.ForeignKey('users.User', on_delete=models.CASCADE)
    categories          = models.ManyToManyField('Category', through='ProgramCategory')
    
    class Meta: 
        db_table = 'programs'

class ProgramCategory(models.Model): 
    program  = models.ForeignKey(Program, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta: 
        db_table = 'program_categories'

class DetailImage(models.Model): 
    image_url = models.CharField(max_length=2000)
    program   = models.ForeignKey('Program', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'detail_images'

class ScreeningQuestion(models.Model): 
    question = models.CharField(max_length=1000)
    program  = models.ManyToManyField('Program', through='ProgramQuestion')

    class Meta: 
        db_table = 'screening_questions'

class ProgramQuestion(models.Model): 
    program  = models.ForeignKey(Program, on_delete=models.CASCADE)
    question = models.ForeignKey(ScreeningQuestion, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'program_questions'

class ScreeningAnswer(models.Model): 
    answer   = models.CharField(max_length=300)
    question = models.ManyToManyField('ScreeningQuestion', through='QuestionAnswer')
    user     = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta: 
        db_table = 'screening_answers'

class QuestionAnswer(models.Model):
    question = models.ForeignKey(ScreeningQuestion, on_delete=models.CASCADE)
    answer   = models.ForeignKey(ScreeningAnswer, on_delete=models.CASCADE)

    class Meta:
        db_table = 'question_answers'

class Logging(TimeStampModel): 
    previous_url = models.CharField(max_length=2000)
    program      = models.ForeignKey(Program, on_delete=models.CASCADE)
    
    class Meta: 
        db_table = 'loggings'