from django.db       import models

from core.models     import TimeStampModel
from programs.models import Program

class User(TimeStampModel):
    kakao_id          = models.CharField(max_length=100, unique = True)
    nickname          = models.CharField(max_length=100)
    email             = models.CharField(max_length=300, null = True)
    profile_image_url = models.CharField(max_length=2000)
    is_host           = models.BooleanField(default=False)
    host_description  = models.CharField(max_length=300, null=True)

    class Meta:
        db_table = 'users'

class Like(models.Model):
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'program_id'], name="unique likes")
        ]

class Review(TimeStampModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user    = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    context = models.CharField(max_length=300)

    class Meta:
        db_table = 'reviews'
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'program_id'], name="unique reviews")
        ]
