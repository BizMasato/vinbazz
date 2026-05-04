from django.db import models
from django.conf import settings
from admin_apps.store.models import Store
from admin_apps.clothes.models import Clothes

""" recommended_clothesテーブル """
class RecommendedClothes(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='recommended_clothes')  # ユーザーID
    clothes_id = models.ForeignKey(Clothes, null=True, blank=True, on_delete=models.CASCADE, related_name='recommended_for_users')  # 商品ID
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'recommended_clothes'
        verbose_name = 'おすすめ商品'
        verbose_name_plural = 'recommended_clothes(おすすめ商品)'

    def __str__(self):
        return f"RecommendedClothes(user={self.user_id}, clothes={self.clothes_id})"

""" recommended_storesテーブル """
class RecommendedStores(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='recommended_stores')  # ユーザーID
    store_id = models.ForeignKey(Store, null=True, blank=True, on_delete=models.CASCADE, related_name='recommended_for_users')  # 店舗ID
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'recommended_stores'
        verbose_name = 'おすすめ店舗'
        verbose_name_plural = 'recommended_stores(おすすめ店舗)'

    def __str__(self):
        return f"RecommendedStores(user={self.user_id}, store={self.store_id})"
