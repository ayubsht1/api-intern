from django.db import models
from django.contrib.auth.models import User

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
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
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
    
class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} to {self.comment.id}"

