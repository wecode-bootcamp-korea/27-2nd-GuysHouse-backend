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
    view                = models.SmallIntegerField(default=0)
    start_date          = models.DateTimeField()
    running_time        = models.PositiveSmallIntegerField()
    user                = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category            = models.ManyToManyField('Category')
    
    class Meta:
        db_table = 'programs'

class DetailImage(models.Model):
    image_url = models.CharField(max_length=2000)
    program   = models.ForeignKey('Program', on_delete=models.CASCADE)

    class Meta:
        db_table = 'detail_images'

class ScreeningQuestion(models.Model):
    question = models.CharField(max_length=1000)
    program  = models.ForeignKey('Program', on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'screening_questions'

class ScreeningAnswer(models.Model):
    answer   = models.CharField(max_length=300)
    question = models.ForeignKey('ScreeningQuestion', on_delete=models.CASCADE)
    user     = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'screening_answers'