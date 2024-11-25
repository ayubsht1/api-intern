from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class SyncDataViewSet(ModelViewSet):
    queryset = SyncData.objects.all()
    serializer_class = SyncDataSerializer

class DashboardViewSet(ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer

class CommunityViewSet(ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class ForumViewSet(ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

class ProgressViewSet(ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

class BookmarkViewSet(ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
