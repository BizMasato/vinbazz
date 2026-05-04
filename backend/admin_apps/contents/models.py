from django.db import models

""" Announcementテーブル """
class Announcement(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    title = models.CharField(max_length=100)  #お知らせのタイトル
    content = models.TextField()  #お知らせの内容
    is_active = models.BooleanField(default=True)  #アクティブフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'announcements'
        verbose_name = 'お知らせ'
        verbose_name_plural = 'announcements(お知らせ)'

    def __str__(self):
        return self.title

""" topicsテーブル """
class Topic(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    title = models.CharField(max_length=100)  #トピックのタイトル
    content = models.TextField()  #トピックの内容
    is_active = models.BooleanField(default=True)  #アクティブフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'topics'
        verbose_name = 'トピック'
        verbose_name_plural = 'topics(トピック)'

    def __str__(self):
        return self.title

""" bannerテーブル """
class Banner(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    title = models.CharField(max_length=100)  #バナーのタイトル
    link = models.URLField()  #バナーのリンク
    display_order = models.IntegerField(default=0)  # 表示順
    is_active = models.BooleanField(default=True)  #アクティブフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'banner'
        verbose_name = 'バナー'
        verbose_name_plural = 'banner(バナー)'

    def __str__(self):
        return self.title
