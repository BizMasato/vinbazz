from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import timedelta
from django.utils import timezone
from datetime import datetime, timedelta, timezone as dt_timezone  # 標準ライブラリのtimezoneをインポート

import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)

    def _num_seconds(self, dt):
        # UTCの1970年1月1日のdatetimeを作成
        epoch = datetime(1970, 1, 1, tzinfo=dt_timezone.utc)  # UTCの1970年エポック
        return int((dt - epoch).total_seconds())

    def make_token(self, user):
        # トークンを生成し、タイムスタンプを含める
        timestamp = self._num_seconds(datetime.now(dt_timezone.utc))  # 現在のUTCタイムスタンプ
        hash_value = self._make_hash_value(user, timestamp)
        return f"{hash_value}:{timestamp}"

    def check_token(self, user, token):
        # トークンのハッシュ部分とタイムスタンプを分離して検証
        try:
            # トークンを分割して、ハッシュ部分とタイムスタンプを取得
            hash_value, timestamp = token.split(':')
            timestamp = int(timestamp)  # タイムスタンプを整数に変換
            
            # ハッシュを生成して、与えられたトークンのハッシュ部分と比較
            expected_hash_value = self._make_hash_value(user, timestamp)
            return hash_value == expected_hash_value
            
        except (ValueError, IndexError):
            return False

    def check_token_expiration(self, token):
        try:
            # トークンからタイムスタンプを取得
            timestamp = self._get_timestamp_from_token(token)
            expiration_time = timedelta(hours=24)  # 有効期間を24時間に設定

            # タイムスタンプをUTCに変換
            token_time = datetime.fromtimestamp(timestamp, tz=dt_timezone.utc)  # 標準ライブラリのtimezoneを使用
            current_time = timezone.now()  # Djangoのタイムゾーン設定に基づいた現在時刻
        
            return (current_time - token_time) < expiration_time
        except (ValueError, TypeError, OverflowError) as e:  # 限定的な例外処理
            return False


    def _get_timestamp_from_token(self, token):
        # トークンを分割して、タイムスタンプを取得
        try:
            # tokenは user.pk と timestamp をつなげたものです
            timestamp = token.split(':')[1]  # ハッシュ部分の後のタイムスタンプ部分を取得
            return int(timestamp)  # タイムスタンプを整数に変換
        except (IndexError, ValueError):
            raise ValueError("Invalid token format")

# インスタンス作成
account_activation_token = AccountActivationTokenGenerator()
