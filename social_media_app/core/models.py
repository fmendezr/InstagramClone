from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile (models.Model):
    id_user = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_imgs/', default='profile_imgs/default_user.svg')
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.user.username