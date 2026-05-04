from django.contrib import admin
from .models import RecommendedClothes, RecommendedStores

@admin.register(RecommendedClothes)
class RecommendedClothesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'clothes_id', 'created_at', 'updated_at')
    search_fields = ('user__email', 'clothes__name')
    list_filter = ('created_at', 'updated_at')

@admin.register(RecommendedStores)
class RecommendedStoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'store_id', 'created_at', 'updated_at')
    search_fields = ('user__email', 'store__name')
    list_filter = ('created_at', 'updated_at')
