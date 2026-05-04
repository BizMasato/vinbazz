"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from admin_apps.clothes.views import save_images
from web_apps.header.views import StoreAreaListView, ClothesCategoryViewSet
from web_apps.banner.views import BannerListView
from web_apps.announcement.views import ActiveAnnouncementsView
from web_apps.user.views import register_user, activate, user_login, check_session, user_logout
from web_apps.clothes.views import ClothesListView, FavoriteClothesView, clothes_breadcrumb
from web_apps.common.common import get_csrf_token
from web_apps.stores.views import store_areas_list, StoresListView, FavoriteStoresView

# 開発環境用
from django.conf import settings
from django.conf.urls.static import static

# 管理画面追加設定
admin.site.site_header = 'vinbazz管理サイト' 
admin.site.index_title = 'メニュー'

urlpatterns = [
    path('admin/', admin.site.urls),  # TODO 開発完了時に変更とセキュリティ対策
    path('save-clothes-images/', save_images, name='save_images'),
    path('api/header/categories/', ClothesCategoryViewSet.as_view({'get': 'list'}), name='get_categories'),  # ヘッダー
    path('api/header/stores/', StoreAreaListView.as_view(), name='get_stores'),  # ヘッダー
    path('api/banners/', BannerListView.as_view(), name='banner-list'),
    path('api/announcements/', ActiveAnnouncementsView.as_view(), name='get_announcements'),
    path('accounts/', include('allauth.urls')),  # allauth のルーティング
    path('api/register/', register_user, name='register_user'),
    path('api/activate/<uidb64>/<token>/', activate, name='activate'),  # 認証リンクのエンドポイント
    path('api/login', user_login, name='login'),
    path('api/check-session', check_session, name='check_session'),
    path('api/logout', user_logout, name='logout'),
    path('api/allclothes/', ClothesListView.as_view(), name='clothes-list'),
    path('api/clothes/favorite/', FavoriteClothesView.as_view(), name='toggle-favorite'),  # お気に入りの登録・解除
    path('api/get-csrf-token/', get_csrf_token, name='get_csrf_token'),  # CSRFトークン取得用エンドポイント
    path('api/areas/', store_areas_list, name='store_areas_list'),
    path('api/stores/', StoresListView.as_view(), name='stores_list'),
    path('api/stores/favorite/', FavoriteStoresView.as_view(), name='toggle-favorite'),  # お気に入りの登録・解除
    path('api/ClothesBreadcrumb/', clothes_breadcrumb, name='clothes_breadcrumb'),
]

# 開発環境用
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
