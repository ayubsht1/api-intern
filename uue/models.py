from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

class SyncData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_type = models.CharField(max_length=100)
    synced_at = models.DateTimeField(auto_now_add=True)

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    widgets = models.JSONField(default=dict)  # Example for storing user-configured dashboard settings

class Community(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='community/thumbnails/')
    tags = models.ManyToManyField('Tag')

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Forum(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=200)
    progress_percent = models.FloatField()

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=100)
    content_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
