from rest_framework import serializers
from .models import (GroupTag, Group, Post, PostLike, Comment, ForumCategory, Forum, ForumReply,
Profile)
from authentication.models import User

class ProfileSerializer(serializers.ModelSerializer):
    share_url = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user','share_url', 'news_interests']
        
    def get_share_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url()) if request else obj.get_share_url()

class GroupTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTag
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=GroupTag.objects.all(), many=True)
    class Meta:
        model = Group
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    created_at = serializers.DateTimeField(read_only=True)
    share_url = serializers.SerializerMethodField()
    like_count= serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'group', 'created_at','share_url', 'like_count']

    def get_share_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url()) if request else obj.get_share_url()

    def get_like_count(self, obj):
        return obj.post_likes.count() 

class PostLikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PostLike
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all()) 
    created_at = serializers.DateTimeField(read_only=True)  

    class Meta:
        model = Comment
        fields = "__all__"

class ForumCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumCategory
        fields = "__all__"

class ForumSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ForumCategory.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Forum
        fields = "__all__"

class ForumReplySerializer(serializers.ModelSerializer):
    forum = serializers.PrimaryKeyRelatedField(queryset=Forum.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = ForumReply
        fields = "__all__"