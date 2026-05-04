# views.py
from rest_framework import generics
from admin_apps.contents.models import Announcement
from .serializers import AnnouncementSerializer

class ActiveAnnouncementsView(generics.ListAPIView):
    queryset = Announcement.objects.filter(is_active=True).order_by('-updated_at')[:3]
    serializer_class = AnnouncementSerializer
