# serializers.py
from rest_framework import serializers
from admin_apps.clothes.models import ClothesCategory
from admin_apps.store.models import Store, StoreArea

class ClothesCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = ClothesCategory
        fields = ['id', 'name', 'children']

    def get_children(self, obj):
        # 子カテゴリを取得
        if obj.children.exists():
            return ClothesCategorySerializer(obj.children.all(), many=True).data
        return []


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name']

class StoreAreaSerializer(serializers.ModelSerializer):
    stores = serializers.SerializerMethodField()

    class Meta:
        model = StoreArea
        fields = ['id', 'name', 'stores']

    def get_stores(self, obj):
        # StoreAreaに紐づくStoreを取得し、is_activeがTrueのものをname順に並べる
        stores = Store.objects.filter(area_id=obj, is_active=True).order_by('name')
        return StoreSerializer(stores, many=True).data
