# urls.py
from django.contrib import admin
from django.urls import path, include
# from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('courses.urls')),  # <-- حولي كل حاجة لـ courses.urls
]