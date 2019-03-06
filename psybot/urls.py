from django.urls import path

from . import views

urlpatterns = [
    path('setemotion/', views.setemotion, name='setemotion'),
    path('classifytext/', views.classifytext, name='classifytext'),
    path('emotionevaluate/', views.emotionevaluate, name='emotionevaluate'),
    path('setspeech/', views.setspeech, name='setspeech'),
    path('register/', views.register, name='register'),
    path('calculate/', views.calculate, name='calculate'),
    path('index/', views.index, name='index'),
]