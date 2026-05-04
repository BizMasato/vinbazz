from django import forms
from django.core.files.storage import FileSystemStorage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import os
from django.utils.safestring import mark_safe
from .models import Banner

class BannerAdminForm(forms.ModelForm):
    # 画像を1枚だけアップロード可能にする
    upload_file = forms.FileField(required=False)

    class Meta:
        model = Banner
        fields = ['title', 'link', 'display_order', 'is_active']

    ''' 後学のために残す。このようにインスタンスの生成後、コミットのタイミングをずらすことが可能(データを加工するときなど)
    def save(self, commit=True):
        instance = super().save(commit=False)  # インスタンスの生成、コミットしない

        # インスタンスを保存してIDを取得
        if commit:
            instance.save()  # ここでコミット
    '''

    def save(self, commit=True):  # ここのコミット指定は意味ないがフォーマット的に記載
        instance = super().save(commit=True)  # インスタンスの生成 + DB更新(id発行・取得)

        # 画像の保存
        if self.cleaned_data.get('upload_file'):
            # 画像を開いてJPEG対応のRGBモードに変換
            file = self.cleaned_data.get('upload_file')
            img = Image.open(file)

            if img.mode in ("RGBA", "LA"):
                img = img.convert("RGB")  # JPEGはRGBモードのみ対応

            max_size = (800, 600)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=80)

            # 古い画像があれば削除
            old_image_path = f'{settings.MEDIA_ROOT}/banner/{instance.id}_1.jpg'
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'banner'))
            if fs.exists(old_image_path):
                fs.delete(old_image_path)

            # 新しい画像を保存
            img_file = ContentFile(img_io.getvalue(), name=f"{instance.id}_1.jpg")
            fs.save(img_file.name, img_file)

        return instance

    def save_m2m(self):  # 処理なしのオーバーライドしないとmodels.pyに記載していないupload_fileのエラーが出力されるため
        pass

    def show_uploaded_image(self):
        if self.instance.id:
            image_url = f'{settings.MEDIA_URL}banner/{self.instance.id}_1.jpg'
            return mark_safe(f'<img src="{image_url}" width="200" />')
        return "No Image Available"
