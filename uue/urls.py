from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'sync-data', SyncDataViewSet)
router.register(r'dashboards', DashboardViewSet)
router.register(r'communities', CommunityViewSet)
router.register(r'forums', ForumViewSet)
router.register(r'progress', ProgressViewSet)
router.register(r'bookmarks', BookmarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]