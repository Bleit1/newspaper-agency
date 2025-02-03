from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # главная страница – список выпусков
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
