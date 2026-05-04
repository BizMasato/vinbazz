# serializers.py
from rest_framework import serializers
from admin_apps.store.models import StoreArea

class StoreAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreArea
        fields = ['id', 'name']
