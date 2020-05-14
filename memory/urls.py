from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('detail', views.detail, name='detail'),
    path('process_image', views.process_image, name='process_image'),
]
