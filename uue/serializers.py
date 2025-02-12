from rest_framework import serializers
from .models import GroupTag, Group, Post, Comment, PostLike, CommentReply
from django.contrib.auth.models import User

class GroupTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTag
        fields = ['id', 'name']

class GroupSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=GroupTag.objects.all(), many=True)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)  

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'created_by', 'members', 'tags']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    created_at = serializers.DateTimeField(read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'group', 'created_at', 'like_count']

    def get_like_count(self, obj):
        return obj.post_likes.count()  # Return the number of likes
    

class PostLikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PostLike
        fields = ['id','post', 'user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all()) 
    created_at = serializers.DateTimeField(read_only=True)  

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'post', 'created_at']

class CommentReplySerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())

    class Meta:
        model = CommentReply
        fields = ['id', 'body', 'author', 'comment', 'created_at']