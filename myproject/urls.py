from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sentiment.urls')),  # Include app-level URLs at the root
]
