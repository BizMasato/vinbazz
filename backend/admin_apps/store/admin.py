from django.contrib import admin
from .models import Prefecture, StoreArea, Store
from .forms import StoreAdminForm
import os
from django.conf import settings
from django.utils.safestring import mark_safe

@admin.register(Prefecture)
class PrefectureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
    ordering = ('id',)

@admin.register(StoreArea)
class StoreAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prefecture_id', 'display_order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('prefecture_id', 'is_active',)
    search_fields = ('name',)
    ordering = ('prefecture_id', 'display_order',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'area_id', 'is_active', 'created_at', 'updated_at')
    list_filter = ('area_id', 'is_active')
    search_fields = ('name',)

    form = StoreAdminForm

    # 編集画面で画像を表示する
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.id:
            form_instance = self.form(instance=obj)
            image_html = form_instance.show_uploaded_image()
            form.base_fields['upload_file'].label = mark_safe(f'Current Image:<br>{image_html}<br>Upload new image:')
        return form

    # 削除時に画像ファイルも削除する
    # 編集画面からの削除
    def delete_model(self, request, obj):
        image_path = f'{settings.MEDIA_ROOT}/store/{obj.id}_1.jpg'
        if os.path.exists(image_path):
            os.remove(image_path)
        super().delete_model(request, obj)

    # 一覧画面からの削除
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            image_path = f'{settings.MEDIA_ROOT}/store/{obj.id}_1.jpg'
            if os.path.exists(image_path):
                os.remove(image_path)
        super().delete_queryset(request, queryset)
