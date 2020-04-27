
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sentiment/', include('sentiment.urls')),
    path('', include('main.urls')),
    path('accounts/', include('allauth.urls')),
    path('tinymce/',include('tinymce.urls')),
]
 