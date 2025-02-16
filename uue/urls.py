from django.urls import path
from uue.views import (
    GroupListCreateView,
    GroupDetailView,
    GroupTagListCreateView,
    GroupTagDetailView,
    PostListCreateView,
    PostDetailView,
    PostLikeView,
    CommentListCreateView,
    CommentDetailView,
    CommentReplyListCreateView,
    CommentReplyDetailView,
    ProfileListCreateView,
    ProfileDetailView,
    ProfileShareView,

)

urlpatterns = [
    path('profiles/', ProfileListCreateView.as_view(), name="profile-list-create"),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name="profile-detail"),
    path('profiles/share/<str:user__username>/', ProfileShareView.as_view(), name="profile-share"),
    path('tags/', GroupTagListCreateView.as_view(), name="tag-list-create"),
    path('tags/<int:pk>/', GroupTagDetailView.as_view(), name="tag-detail"),
    path('groups/', GroupListCreateView.as_view(), name="group-list-create"),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name="group-detail"),  
    path('posts/', PostListCreateView.as_view(), name="post-list-create"),
    path('posts/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('posts/<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),  # To like/unlike a post
    path('comments/', CommentListCreateView.as_view(), name="comment-list-create"),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name="comment-detail"),
    path('comments-replies/', CommentReplyListCreateView.as_view(), name='comment-reply-list-create'),
    path('comments-replies/<int:pk>/', CommentReplyDetailView.as_view(), name='comment-reply-detail'),
]
