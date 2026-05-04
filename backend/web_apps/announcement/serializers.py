# serializers.py
from rest_framework import serializers
from admin_apps.contents.models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'updated_at']
