from . import views
from django.urls import path

app_name = 'write'

urlpatterns = [
    
    path('', views.home, name='home'),
]