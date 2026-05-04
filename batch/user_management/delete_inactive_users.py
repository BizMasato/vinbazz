# batch/user_management/delete_inactive_users.py
import os
import sys
import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

# プロジェクトのルートディレクトリを取得
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 3階層上を指定

# Djangoプロジェクトの設定を読み込む
sys.path.append(os.path.join(BASE_DIR, 'backend'))  # backendフォルダをパスに追加
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # settings.pyのパスを指定

import django
django.setup()

def delete_inactive_users():
    # 現在の時刻から48時間前を計算
    time_threshold = timezone.now() - datetime.timedelta(hours=48)
    User = get_user_model()

    # 48時間以上経過しているかつis_activeがFalseのユーザーをフィルター
    inactive_users = User.objects.filter(is_active=False, created_at__lte=time_threshold)

    # 削除するユーザーのIDとメールアドレスを取得
    user_info = [(user.id, user.email) for user in inactive_users]

    # 削除処理
    count, _ = inactive_users.delete()

    # 結果を表示
    print(f"{count} users deleted.")
    if user_info:
        print("Deleted users:")
        for user_id, email in user_info:
            print(f"ID: {user_id}, Email: {email}")

if __name__ == "__main__":
    delete_inactive_users()
