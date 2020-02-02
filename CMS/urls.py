from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('setlog/', views.setlog, name='setlog'),
    path('ner/', views.ner, name='ner'),
]
