# serializers.py
from rest_framework import serializers
from admin_apps.contents.models import Banner
from django.conf import settings

class BannerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['id', 'title', 'link', 'image_url']

    def get_image_url(self, obj):
        # DjangoのMEDIA_URLを使用して画像のURLを構築
        request = self.context.get('request')
        return request.build_absolute_uri(settings.MEDIA_URL + 'banner/' + str(obj.id) + '_1.jpg')
