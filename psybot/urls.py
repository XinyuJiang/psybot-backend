from django.urls import path

from . import views

urlpatterns = [
    path('emotion_analyze/', views.emotion_analyze, name='emotion_analyze'),
    path('biclassifyemotion/', views.biclassifyemotion, name='biclassifyemotion'),
    path('setemotion/', views.setemotion, name='setemotion'),
    path('classifytext/', views.classifytext, name='classifytext'),
    path('emotionevaluate/', views.emotionevaluate, name='emotionevaluate'),
    path('setspeech/', views.setspeech, name='setspeech'),
    path('register/', views.register, name='register'),
    path('calculate/', views.calculate, name='calculate'),
    path('index/', views.index, name='index'),
]