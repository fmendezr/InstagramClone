from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

# Create your models here.
class Profile (models.Model):
    id_user = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to='profile_imgs/', default='profile_imgs/default_user.svg')
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.user.username
    
class Post (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    caption = models.CharField(max_length=280)
    created = models.DateTimeField(default=datetime.now)
    no_likes = models.IntegerField(default=0)
    
class LikePost (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class SavePost (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FollowerCount (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)