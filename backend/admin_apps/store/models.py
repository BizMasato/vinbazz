from django.db import models

""" prefecturesテーブル """
class Prefecture(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    name = models.CharField(max_length=100)  # 都道府県名
    is_active = models.BooleanField(default=True)  # アクティブフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'prefectures'
        verbose_name = '都道府県'
        verbose_name_plural = 'prefectures(都道府県)'

    def __str__(self):
        return self.name

""" store_areasテーブル """
class StoreArea(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    name = models.CharField(max_length=100)  # エリア名
    prefecture_id = models.ForeignKey(Prefecture, on_delete=models.SET_NULL, null=True, blank=True, related_name='areas_in_prefecture')  # 都道府県ID
    display_order = models.IntegerField(default=0)  # 表示順
    is_active = models.BooleanField(default=True)  # アクティブフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'store_areas'
        verbose_name = '店舗エリア'
        verbose_name_plural = 'store_areas(店舗エリア)'

    def __str__(self):
        return self.name

""" storesテーブル """
class Store(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    name = models.CharField(max_length=100)  # 店舗名
    area_id = models.ForeignKey(StoreArea, on_delete=models.SET_NULL, null=True, blank=True, related_name='stores_in_area')  # エリアID
    description = models.TextField(blank=True)  # 店舗説明
    website_url = models.URLField(blank=True)  # サイトURL
    instagram_url = models.URLField(blank=True)  # InstagramのURL
    is_active = models.BooleanField(default=True)  # アクティブフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        db_table = 'stores'
        verbose_name = '店舗'
        verbose_name_plural = 'stores(店舗)'

    def __str__(self):
        return self.name