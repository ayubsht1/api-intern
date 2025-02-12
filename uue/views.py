from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Comment, Group, GroupTag, PostLike, CommentReply
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer, GroupTagSerializer,
    PostLikeSerializer, CommentReplySerializer)

class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [IsAuthenticated]

class GroupTagListCreateView(generics.ListCreateAPIView):
    queryset = GroupTag.objects.all()
    serializer_class = GroupTagSerializer
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save()

class GroupTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupTag.objects.all()
    serializer_class = GroupTagSerializer
    # permission_classes = [IsAuthenticated]


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]
    # def get_queryset(self):
    #     return Post.objects.filter(author=self.request.user)

class PostLikeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeSerializer

    def post(self, request, post_id):
        """
        Like a post (Create a PostLike).
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if PostLike.objects.filter(post=post, user=user).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        PostLike.objects.create(post=post, user=user)

        return Response({"message": "Post liked successfully!", "like_count": post.post_likes.count()}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        """
        Unlike a post (Delete the PostLike).
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        try:
            post_like = PostLike.objects.get(post=post, user=user)
            post_like.delete()
            return Response({"message": "Post unliked successfully!", "like_count": post.post_likes.count()}, status=status.HTTP_200_OK)
        except PostLike.DoesNotExist:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     user=self.request.user
    #     serializer.save(username=user.username, author=user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]
    # def get_queryset(self):
    #     return Post.objects.filter(userId=self.request.user)

class CommentReplyListCreateView(generics.ListCreateAPIView):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

class CommentReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    # permission_classes = [IsAuthenticated]