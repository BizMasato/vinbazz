from django.contrib import admin
from .models import Batches, BatchProcesses

@admin.register(Batches)
class BatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name', 'store_id', 'is_active', 'execution_order', 'created_at', 'updated_at')
    list_filter = ('is_active', 'store_id')

@admin.register(BatchProcesses)
class BatchProcessesAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch_id', 'status', 'start_time', 'end_time', 'created_at', 'updated_at')
    list_filter = ('status', 'batch_id')
