from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from admin_apps.clothes.models import Clothes, ClothesCategory
from admin_apps.store.models import Store, StoreArea
from admin_apps.user.models import FavoriteClothes
from django.http import JsonResponse
from django.conf import settings

class ClothesListView(APIView):
    def get(self, request):

        # クエリパラメータの取得
        store_id = request.GET.get('store_id')
        area_id = request.GET.get('area_id')
        category_id = request.GET.get('category_id')

        clothes_list = []
        clothes = Clothes.objects.filter(is_active=True).order_by('-updated_at').select_related('store_id').filter(is_active=True)  # 全商品とそれに紐づく店舗を取得
        # TODO updated_atの降順は切り替えられるようにする

        # クエリパラメータが存在する場合にフィルタリング
        if store_id:
            clothes = clothes.filter(store_id=store_id)
        if area_id:
            clothes = clothes.filter(store_id__area_id=area_id)
        if category_id:
            # 親カテゴリーが指定された場合、子カテゴリーも含める
            selected_category = ClothesCategory.objects.filter(id=category_id).first()
            if selected_category:
                # 親と子カテゴリーIDを取得
                category_ids = [selected_category.id] + list(
                    ClothesCategory.objects.filter(parent_id=category_id).values_list('id', flat=True)
                )
                clothes = clothes.filter(category_id__in=category_ids)

        for item in clothes:
            is_favorite = False  # 初期値はFalse

            # ユーザーがログインしているか確認
            if request.user.is_authenticated:
                is_favorite = FavoriteClothes.objects.filter(user_id=request.user, clothes_id=item.id).exists()  # ログインユーザーの場合

            clothes_list.append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'image': request.build_absolute_uri(settings.MEDIA_URL + 'clothes/' + str(item.id) + '/' + str(item.id) + '_1.jpg'),
                'is_favorite': is_favorite,
                'store': {
                    'id': item.store_id.id,
                    'name': item.store_id.name,
                }
            })

        return Response(clothes_list)


class FavoriteClothesView(APIView):
    permission_classes = [IsAuthenticated]  # 認証されたユーザーのみ

    def post(self, request):
        clothes_id = request.data.get('item_id')  # フロントエンドからのIDを取得

        if not clothes_id:
            return Response({'error': 'clothes_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Clothesインスタンスを取得
        clothes_instance = get_object_or_404(Clothes, id=clothes_id)
        # お気に入りの登録
        favorite, created = FavoriteClothes.objects.get_or_create(user_id=request.user, clothes_id=clothes_instance)

        if created:
            return Response({'message': 'Added to favorites.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already in favorites.'}, status=status.HTTP_200_OK)


    def delete(self, request):
        clothes_id = request.data.get('item_id')

        if not clothes_id:
            return Response({'error': 'clothes_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite = FavoriteClothes.objects.get(user_id=request.user, clothes_id=clothes_id)
            favorite.delete()
            return Response({'message': 'Removed from favorites.'}, status=status.HTTP_204_NO_CONTENT)
        except FavoriteClothes.DoesNotExist:
            return Response({'error': 'Favorite not found.'}, status=status.HTTP_404_NOT_FOUND)


def clothes_breadcrumb(request):

    # クエリパラメータの取得
    store_id = request.GET.get('store_id')
    area_id = request.GET.get('area_id')
    category_id = request.GET.get('category_id')

    # パンくずリストのデータを格納する辞書
    breadcrumb_data = {}

    # store_id が渡された場合
    if store_id:
        store = get_object_or_404(Store, id=store_id)
        breadcrumb_data = {
            "type": "store",
            "title": "【古着屋：" + store.name +   "の商品】",
            "id": store.id,
            "name": store.name
        }

    # area_id が渡された場合
    elif area_id:
        area = get_object_or_404(StoreArea, id=area_id)
        breadcrumb_data = {
            "type": "area",
            "title": "【古着屋エリア：" + area.name +   "の商品】",
            "id": area.id,
            "name": area.name
        }

    # category_id が渡された場合
    elif category_id:
        category = get_object_or_404(ClothesCategory, id=category_id)
        hierarchy = []
        current_category = category

        # 親子関係を遡ってパンくずリストを作成
        last_category_name = ''
        while current_category:
            hierarchy.insert(0, {"id": current_category.id, "name": current_category.name})
            last_category_name = current_category.name  # 最後のカテゴリーをタイトルに含める
            current_category = current_category.parent_id

        breadcrumb_data = {
            "type": "category",
            "title": "【カテゴリー：" + last_category_name +   "の商品】",
            "hierarchy": hierarchy
        }

    return JsonResponse(breadcrumb_data)
