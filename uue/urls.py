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
    ForumCategoryListCreateView,
    ForumCategoryDetailView,
    ForumListCreateView,
    ForumDetailView,
    ForumReplyListCreateView,
    ForumReplyDetailView,
    ProfileListCreateView,
    ProfileDetailView,
)

urlpatterns = [
    path('profiles/', ProfileListCreateView.as_view(), name="profile-list-create"),
    path('profiles/<slug:slug>/', ProfileDetailView.as_view(), name="profile-detail"),
    path('tags/', GroupTagListCreateView.as_view(), name="tag-list-create"),
    path('tags/<int:pk>/', GroupTagDetailView.as_view(), name="tag-detail"),
    path('groups/', GroupListCreateView.as_view(), name="group-list-create"),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name="group-detail"),  
    path('posts/', PostListCreateView.as_view(), name="post-list-create"),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name="post_detail"),
    path('posts/<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),  # To like/unlike a post
    path('comments/', CommentListCreateView.as_view(), name="comment-list-create"),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name="comment-detail"),
    path('categories/', ForumCategoryListCreateView.as_view(), name='forum-category-list-create'),
    path('categories/<int:pk>/', ForumCategoryDetailView.as_view(), name='forum-category-detail'),
    path('forums/', ForumListCreateView.as_view(), name='forum-list-create'),
    path('forums/<int:pk>/', ForumDetailView.as_view(), name='forum-detail'),
    path('forums-replies/', ForumReplyListCreateView.as_view(), name='forum-post-list-create'),
    path('forums-replies/<int:pk>/', ForumReplyDetailView.as_view(), name='forum-post-detail'),

]
