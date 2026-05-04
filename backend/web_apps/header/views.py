# views.py
from rest_framework import generics, viewsets
from rest_framework.response import Response
from admin_apps.clothes.models import ClothesCategory
from admin_apps.store.models import StoreArea
from .serializers import StoreAreaSerializer, ClothesCategorySerializer

class ClothesCategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        # is_activeがTrueの親カテゴリを取得し、display_order順にソート
        categories = ClothesCategory.objects.filter(is_active=True, parent_id__isnull=True).prefetch_related('children')
        serializer = ClothesCategorySerializer(categories, many=True)
        return Response(serializer.data)

class StoreAreaListView(generics.ListAPIView):
    serializer_class = StoreAreaSerializer

    def get_queryset(self):
        return StoreArea.objects.filter(is_active=True).order_by('display_order')
