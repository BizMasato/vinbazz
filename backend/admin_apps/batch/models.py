from django.db import models
from admin_apps.store.models import Store

""" batchesテーブル """
class Batches(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    name = models.CharField(max_length=100)  # バッチ名
    store_id = models.ForeignKey(Store, null=True, blank=True, on_delete=models.SET_NULL, related_name='batches')  # 店舗ID
    is_active = models.BooleanField(default=True)  # アクティブフラグ
    execution_order = models.IntegerField(default=0)  # 実行順
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'batches'
        verbose_name = 'バッチ'
        verbose_name_plural = 'batches(バッチ)'

    def __str__(self):
        return f"{self.name} (Store: {self.store_id.name}, Order: {self.execution_order})"

""" batch_processesテーブル """
class BatchProcesses(models.Model):
    id = models.AutoField(primary_key=True)  # 自動生成される主キー
    batch_id = models.ForeignKey(Batches, null=True, blank=True, on_delete=models.SET_NULL, related_name='batch_processes')  # バッチID
    start_time = models.DateTimeField()  # 開始日付
    end_time = models.DateTimeField(null=True, blank=True)  # 終了日付
    status = models.CharField(max_length=50, choices=[
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ], default='PENDING')  # ステータス
    error_message = models.TextField(blank=True)  # エラーメッセージ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日付
    updated_at = models.DateTimeField(auto_now=True)  # 更新日付

    class Meta:
        db_table = 'batch_processes'
        verbose_name = 'バッチ処理状況'
        verbose_name_plural = 'batch_processes(バッチ処理状況)'

    def __str__(self):
        return f"BatchProcess(batch={self.batch_id.name}, status={self.status})"
