from django.contrib import admin
from .models import Clothes, ClothesCategory, ClothesBrand
import os
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

@admin.register(ClothesBrand)
class ClothesBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(ClothesCategory)
class ClothesCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_id', 'display_order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('parent_id',)

@admin.register(Clothes)
class ClothesAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_clothes_id', 'name', 'store_id', 'category_id', 'brand_id', 'price', 'sex', 'is_active', 'created_at', 'updated_at')
    search_fields = ('id', 'original_clothes_id', 'name', 'description')
    list_filter = ('store_id', 'category_id', 'brand_id', 'sex')

    change_form_template = 'admin/clothes/clothes_change_form.html'  # カスタムテンプレートのパス

    # 編集画面表示時に画像を表示する
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # オリジナルの変更ビューのコンテキストを拡張する
        if not extra_context:
            extra_context = {}

        # 画像ディレクトリのパス
        image_dir = os.path.join(settings.MEDIA_ROOT, 'clothes', str(object_id))
        image_url = os.path.join(settings.MEDIA_URL, 'clothes', str(object_id))  # フロントエンドからの参照用
        # 画像ファイルを取得
        if os.path.exists(image_dir):
            # TODO 隠しファイルを除くのはmac用(.DS_Storeが作成されてしまうため)
            #image_files = sorted(os.listdir(image_dir))  # ファイル名でソート            
            image_files = sorted([filename for filename in os.listdir(image_dir) if not filename.startswith('.')])  # ファイル名でソート(隠しファイルを除く)
            extra_context['image_files'] = image_files  # コンテキストに追加
            extra_context['image_dir'] = image_url  # コンテキストに追加

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


    # 削除時に画像ファイルも削除する
    # 編集画面からの削除
    def delete_model(self, request, obj):
        image_path = os.path.join(settings.MEDIA_ROOT, 'clothes', str(obj.id))
        if os.path.exists(image_path):
            for file in os.listdir(image_path):
                os.remove(os.path.join(image_path, file))
            os.rmdir(image_path)
        super().delete_model(request, obj)


    # 一覧画面からの削除
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)
        super().delete_queryset(request, queryset)
