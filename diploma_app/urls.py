from django.urls import path, include
from django.contrib import admin

urlpatterns = [
     path("admin/", admin.site.urls),
     path("api/v1/", include('app.urls', namespace='app')),
     path("social/", include('rest_framework_social_oauth2.urls', namespace='social'))
 ]
