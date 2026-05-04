from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from admin_apps.store.models import Store, StoreArea
from .serializers import StoreAreaSerializer
from admin_apps.user.models import FavoriteStores
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.conf import settings

@api_view(['GET'])
def store_areas_list(request):

    storeAreas = StoreArea.objects.filter(is_active=True)
    serializer = StoreAreaSerializer(storeAreas, many=True)

    return Response(serializer.data)


class StoresListView(APIView):
    def get(self, request):
        stores_list = []
        area_id = request.query_params.get('area')
        if area_id:
            stores = Store.objects.filter(area_id=area_id, is_active=True)
        else:
            stores = Store.objects.filter(is_active=True)

        for item in stores:
            is_favorite = False  # 初期値はFalse

            # ユーザーがログインしているか確認
            if request.user.is_authenticated:
                is_favorite = FavoriteStores.objects.filter(user_id=request.user, store_id=item.id).exists()  # ログインユーザーの場合

            stores_list.append({
                'id': item.id,
                'name': item.name,
                'image': request.build_absolute_uri(settings.MEDIA_URL + 'store/' + str(item.id) + '_1.jpg'),
                'is_favorite': is_favorite,
            })

        return Response(stores_list)


class FavoriteStoresView(APIView):
    permission_classes = [IsAuthenticated]  # 認証されたユーザーのみ

    def post(self, request):
        store_id = request.data.get('item_id')  # フロントエンドからのIDを取得

        if not store_id:
            return Response({'error': 'store_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Clothesインスタンスを取得
        store_instance = get_object_or_404(Store, id=store_id)
        # お気に入りの登録
        favorite, created = FavoriteStores.objects.get_or_create(user_id=request.user, store_id=store_instance)

        if created:
            return Response({'message': 'Added to favorites.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already in favorites.'}, status=status.HTTP_200_OK)


    def delete(self, request):
        store_id = request.data.get('item_id')

        if not store_id:
            return Response({'error': 'store_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite = FavoriteStores.objects.get(user_id=request.user, store_id=store_id)
            favorite.delete()
            return Response({'message': 'Removed from favorites.'}, status=status.HTTP_204_NO_CONTENT)
        except FavoriteStores.DoesNotExist:
            return Response({'error': 'Favorite not found.'}, status=status.HTTP_404_NOT_FOUND)


def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})
