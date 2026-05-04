from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from admin_apps.store.models import Store
from admin_apps.clothes.models import Clothes

""" usersテーブル """
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    email = models.EmailField(unique=True)  # ユニークなメールフィールド
    password = models.CharField(max_length=128)  # パスワード(再定義)
    username = models.CharField(blank=True, null=True)
    is_active = models.BooleanField(default=True)  # アクティブ
    is_staff = models.BooleanField(default=False)  # 管理サイトログイン
    is_superuser = models.BooleanField(default=False)  # 管理者権限(再定義)
    last_login = models.DateTimeField(null=True, blank=True)  # 最終ログイン日時
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'ユーザー'
        verbose_name_plural = 'users(ユーザー)'

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email.split('@')[0]  # メールアドレスのローカル部を取得
        super().save(*args, **kwargs)

""" favorite_clothesテーブル """
class FavoriteClothes(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='favorite_clothes')  # ユーザーID
    clothes_id = models.ForeignKey(Clothes, null=True, blank=True, on_delete=models.CASCADE, related_name='favorited_by')  # 商品ID
    status = models.CharField(max_length=50, choices=[
        ('IN_STOCK', 'IN STOCK'),
        ('SOLD_OUT', 'SOLD OUT'),
    ], default='IN_STOCK')  # ステータス
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'favorite_clothes'
        verbose_name = 'お気に入り商品'
        verbose_name_plural = 'favorite_clothes(お気に入り商品)'

    def __str__(self):
        return f"FavoriteClothes(user={self.user_id.email}, clothes={self.clothes_id.name}, status={self.status})"

""" favorite_storesテーブル """
class FavoriteStores(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='favorite_stores')  # ユーザーID
    store_id = models.ForeignKey(Store, null=True, blank=True, on_delete=models.CASCADE, related_name='favorited_by')  # 店舗ID
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'favorite_stores'
        verbose_name = 'お気に入り店舗'
        verbose_name_plural = 'favorite_stores(お気に入り店舗)'

    def __str__(self):
        return f"FavoriteStores(user={self.user_id.email}, store={self.store_id.name})"

""" search_historiesテーブル """
class SearchHistory(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='search_histories')  # ユーザーID
    search_term = models.CharField(max_length=255)  # 検索語句
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'search_histories'
        verbose_name = '検索履歴'
        verbose_name_plural = 'search_histories(検索履歴)'

    def __str__(self):
        return f"SearchHistory(user={self.user_id.email}, search_term={self.search_term})"

""" view_historiesテーブル """
class ViewHistory(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='view_histories')  # ユーザーID
    clothes_id = models.ForeignKey(Clothes, null=True, blank=True, on_delete=models.CASCADE, related_name='viewed_by')  # 商品ID
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'view_histories'
        verbose_name = '閲覧履歴'
        verbose_name_plural = 'view_histories(閲覧履歴)'

    def __str__(self):
        return f"ViewHistory(user={self.user_id.email}, clothes={self.clothes_id.name})"
