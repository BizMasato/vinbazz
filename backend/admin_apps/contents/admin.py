from django.contrib import admin
from .models import Announcement, Topic, Banner
from .forms import BannerAdminForm
import os
from django.conf import settings
from django.utils.safestring import mark_safe

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('is_active', 'created_at', 'updated_at')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('is_active', 'created_at', 'updated_at')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):

    form = BannerAdminForm

    # 編集画面で画像を表示する
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.id:
            form_instance = self.form(instance=obj)
            image_html = form_instance.show_uploaded_image()
            form.base_fields['upload_file'].label = mark_safe(f'Current Image:<br>{image_html}<br>Upload new image:')
        return form

    list_display = ('id', 'title', 'link', 'display_order', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'link')
    list_filter = ('is_active', 'created_at', 'updated_at')

    # 削除時に画像ファイルも削除する
    def delete_model(self, request, obj):
        image_path = f'{settings.MEDIA_ROOT}/banner/{obj.id}_1.jpg'
        if os.path.exists(image_path):
            os.remove(image_path)
        super().delete_model(request, obj)

    # 一覧画面からの削除
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            image_path = f'{settings.MEDIA_ROOT}/banner/{obj.id}_1.jpg'
            if os.path.exists(image_path):
                os.remove(image_path)
        super().delete_queryset(request, queryset)
