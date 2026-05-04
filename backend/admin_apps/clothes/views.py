#from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
from config import settings
import os
import shutil

def save_images(request):
    if request.method == 'POST':

        # 一時ファイル名と元のファイル名を対応させる辞書
        temp_files = {}
        allowed_files = set()
        image_folder = f'{settings.MEDIA_ROOT}/clothes/{request.POST.get("object_id")}/'

        # FileSystemStorageのインスタンス
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'clothes', str(request.POST.get("object_id"))))

        # 新しい画像を一時ファイル名で保存
        for idx, image_file in enumerate(request.FILES.getlist('image-input'), start=1):

            # 既存の画像は保管先から読み込む
            if image_file.size == 0:  # 既存のファイルの場合
                existing_path = os.path.join(image_folder, image_file.name)
                img = Image.open(existing_path)
            else:
                img = Image.open(image_file)
            
            # サイズや解像度を変更
            if img.mode in ("RGBA", "LA"):
                img = img.convert("RGB")
            max_size = (800, 600)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存処理
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=80)
            img_filename = f'{request.POST.get("object_id")}_{idx}.jpg'
            allowed_files.add(img_filename)  # 保存予定のファイルを追加

            if fs.exists(img_filename):
                # ファイルが存在する場合、一時ファイル名を作成
                base_name, ext = os.path.splitext(img_filename)
                temp_filename = f"{base_name}_temp{ext}"

                # 一時ファイルとして保存
                img_file_temp = ContentFile(img_io.getvalue(), name=temp_filename)
                fs.save(temp_filename, img_file_temp)
                print(f"Saved {img_filename} as {temp_filename}")

                # 一時ファイル名と元のファイル名を対応付ける
                temp_files[temp_filename] = img_filename
            else:
                # ファイルが存在しない場合、そのまま保存
                img_file = ContentFile(img_io.getvalue(), name=img_filename)
                fs.save(img_file.name, img_file)
                print(f"Saved {img_filename} as {img_filename}")

        # すべてのファイルが保存された後の処理
        # 1. 一時ファイル名を元のファイル名に戻す
        for temp_filename, original_filename in temp_files.items():
            fs.delete(original_filename)  # 既存のファイルを削除
            fs.save(original_filename, fs.open(temp_filename))  # 一時ファイルを元の名前で保存
            fs.delete(temp_filename)  # 一時ファイルを削除
            print(f"Renamed {temp_filename} to {original_filename}")

        # 2. 保存したファイル以外を削除
        for filename in os.listdir(image_folder):
            file_path = os.path.join(image_folder, filename)
            if filename not in allowed_files and os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")        

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
