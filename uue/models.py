from django.db import models
from authentication.models import User
from django.utils.text import slugify
from django.urls import reverse
# from elearning.models import CourseProgress

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    # learning_progress = models.ForeignKey(CourseProgress, on_delete=models.CASCADE, blank=True, null=True)
    news_interests = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=False, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'slug': self.slug})
    
    def get_share_url(self):
        return f'http://127.0.0.1:8000/uue/profiles/{self.get_absolute_url()}'

    def __str__(self):
        return self.user.username
    
class GroupTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100 , unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='joined_groups', blank=True)
    tags = models.ManyToManyField(GroupTag, related_name='groups', blank=True)
    # thumbnail = models.ImageField(upload_to='group_thumbnails', blank=True, null=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])
    
    def get_share_url(self):
        return f'http://127.0.0.1:8000/uue/posts/{self.get_absolute_url()}'
    
    def __str__(self):
        return f"Post {self.title} in {self.group.name}"
    
    def likes_count(self):
        return self.post_likes.count()
    
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.post.title[:15]}"
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.author.username} commented on {self.body[:15]}... on {self.post.title[:10]}..."
    
class ForumCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Forum(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ForumReply(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Replied by {self.author.username} in {self.forum.title}"