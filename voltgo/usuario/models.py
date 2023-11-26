from django.db import models
from django.conf import settings

class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    direction = models.CharField(blank=True, max_length=100)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)

    def __str__(self):
        return 'Profile for user {self.user.username}'
