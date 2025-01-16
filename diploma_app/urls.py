from app.custom_views import  auth_complete
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
     path("admin/", admin.site.urls),
     # 'auth_complete' will return internal token by redirect
     path("auth_complete/", auth_complete, name='auth_complete'),
     # social backends
     path("social/", include('social_django.urls',namespace='social')), 
     path("auth/", include('drf_social_oauth2.urls', namespace='drf')),
     # general API
     path("api/v1/", include('app.urls', namespace='app')),
]
