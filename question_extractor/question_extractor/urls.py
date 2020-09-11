"""
Endpoint configuration.

"""
from django.contrib import admin
from django.urls import path
from .views import extract, home, answer


urlpatterns = [
    path('admin/', admin.site.urls),
    path('extract/', extract),
    path('', home),
    path('answer/', answer)
]
