from django import forms
from django.core.files.storage import FileSystemStorage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.utils.safestring import mark_safe
from .models import Clothes

class ClothesAdminForm(forms.ModelForm):

    class Meta:
        model = Clothes
        fields = ['original_clothes_id', 'store_id', 'category_id', 'brand_id', 'sex', 'name', 'price', 'description', 'is_active', 'url', 'is_active']

    class Media:
        js = ('js/clothes_preview.js',)  # 新しいJavaScriptファイルを追加

    def save(self, commit=True):
        instance = super().save(commit=commit)

        # 画像の保存
        if self.cleaned_data.get('upload_file'):
            files = self.cleaned_data['upload_file']
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'clothes', str(instance.id)))

            # すでに存在する画像を削除
            existing_files = fs.listdir('')[1]
            for existing_file in existing_files:
                if existing_file.startswith(f"{instance.id}_"):
                    fs.delete(existing_file)

            # 新しい画像を保存
            for i, file in enumerate(files):
                img = Image.open(file)
                if img.mode in ("RGBA", "LA"):
                    img = img.convert("RGB")
                max_size = (800, 600)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=80)
                img_file = ContentFile(img_io.getvalue(), name=f"{instance.id}_{i + 1}.jpg")
                fs.save(img_file.name, img_file)

        return instance

    def save_m2m(self):
        pass

    def show_uploaded_image(self):
        if self.instance.id:
            images = []
            image_url_base = f'{settings.MEDIA_URL}clothes/{self.instance.id}/'
        # 既存の画像をすべて取得
        for i in range(1, 100):  # 最大100枚の画像を想定
            image_path = os.path.join(settings.MEDIA_ROOT, 'clothes', str(self.instance.id), f"{self.instance.id}_{i}.jpg")
            if os.path.exists(image_path):  # 画像ファイルが存在する場合のみ追加
                images.append(f'<img src="{image_url_base}{self.instance.id}_{i}.jpg" width="200" />')
            else:
                break  # 画像が存在しない場合はループを終了
        return mark_safe('<br>'.join(images)) if images else "No Image Available"
