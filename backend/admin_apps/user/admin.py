from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from .models import CustomUser, FavoriteClothes, FavoriteStores, SearchHistory, ViewHistory

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'username', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'created_at', 'updated_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # 追加処理時、現在の管理者がis_superuserかどうかを確認
        if not request.user.is_superuser:
            raise ValidationError("ユーザーを追加できるのはスーパーユーザーのみです")

        obj.set_password(obj.password)  # パスワードをハッシュ化して保存
        super().save_model(request, obj, form, change)

@admin.register(FavoriteClothes)
class FavoriteClothesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'clothes_id', 'status', 'created_at', 'updated_at')
    search_fields = ('user__email', 'clothes__name')
    list_filter = ('status', 'created_at', 'updated_at')

@admin.register(FavoriteStores)
class FavoriteStoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'store_id', 'created_at', 'updated_at')
    search_fields = ('user__email', 'store__name')
    list_filter = ('created_at', 'updated_at')

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'search_term', 'created_at', 'updated_at')
    search_fields = ('user__email', 'search_term')
    list_filter = ('created_at', 'updated_at')

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'clothes_id', 'created_at', 'updated_at')
    search_fields = ('user__email', 'clothes__name')
    list_filter = ('created_at', 'updated_at')
