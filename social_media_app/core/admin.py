from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.LikePost)
admin.site.register(models.FollowerCount)
admin.site.register(models.SavePost)
admin.site.register(models.CommentPost)