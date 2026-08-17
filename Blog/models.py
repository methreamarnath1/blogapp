from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    fullname = models.CharField(max_length=30, null=False, blank=False)
    profile_pic = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE   
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.fullname.upper()

class Blog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    description = models.TextField(max_length=1000)

    blog_poster = models.ImageField(
        upload_to='blog_posters/'
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title[:71]