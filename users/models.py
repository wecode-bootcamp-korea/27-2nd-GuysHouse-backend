from django.db import models

from core.models import TimeStampModel
from programs.models import Program

class User(TimeStampModel):
    nickname = models.CharField(max_length=100)
    email = models.CharField(max_length=300, unique=True)
    profile_image_url = models.CharField(max_length=2000)
    host = models.BooleanField(default=False)
    host_description = models.CharField(max_length=300, null=True)

    class Meta:
        db_table = 'users'

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

class Review(TimeStampModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    context = models.CharField(max_length=300)

    class Meta:
        db_table = 'reviews'
