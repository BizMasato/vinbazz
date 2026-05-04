from django.db import models
from admin_apps.store.models import Store
from django.core.validators import MinValueValidator

""" clothes_categoriesテーブル """
class ClothesCategory(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    name = models.CharField(max_length=100)  # カテゴリ名
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children',)
    display_order = models.IntegerField(default=0)  # 表示順
    is_active = models.BooleanField(default=True)  # アクティブフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'clothes_categories'
        verbose_name = '商品カテゴリ'
        verbose_name_plural = 'clothes_categories(商品カテゴリ)'

    def __str__(self):
        return self.name

""" clothes_brandsテーブル """
class ClothesBrand(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    name = models.CharField(max_length=100)  # ブランド名
    is_active = models.BooleanField(default=True)  # アクティブフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'clothes_brands'
        verbose_name = '商品ブランド'
        verbose_name_plural = 'clothes_brands(商品ブランド)'

    def __str__(self):
        return self.name

""" clothesテーブル """
class Clothes(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    original_clothes_id = models.CharField(max_length=255, unique=True)  # オリジナルID
    store_id = models.ForeignKey(Store, null=True, blank=True, on_delete=models.SET_NULL, related_name='clothes_in_store')  # 店舗ID
    category_id = models.ForeignKey('ClothesCategory', null=True, blank=True, on_delete=models.SET_NULL, related_name='clothes_in_category')  # カテゴリーID
    brand_id = models.ForeignKey('ClothesBrand', null=True, blank=True, on_delete=models.SET_NULL, related_name='clothes_in_brand')  # ブランドID
    sex = models.CharField(max_length=1, choices=[
        ('', '-'),  # 空白の選択肢
        ('M', 'MENS'),
        ('F', 'LADIES'),
        ('U', 'MENS/LADIES'),
    ], blank=True)  # 性別
    name = models.CharField(max_length=255)  # 商品名
    price = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)])  # 商品価格
    description = models.TextField()  # 商品説明
    url = models.URLField()  # URL
    is_active = models.BooleanField(default=True)  # アクティブフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'clothes'
        verbose_name = '商品'
        verbose_name_plural = 'clothes(商品)'

    def __str__(self):
        return self.name
