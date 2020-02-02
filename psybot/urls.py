from django.urls import path

from . import views

urlpatterns = [
    path('getusertext/', views.getusertext, name='getusertext'),
    path('setopinion/', views.setopinion, name='setopinion'),
    path('getuserid/', views.getuserid, name='getuserid'),
    path('calcmingxiang/', views.calcmingxiang, name='calcmingxiang'),
    path('setmingxiang/', views.setmingxiang, name='setmingxiang'),
    path('emotion_analyze/', views.emotion_analyze, name='emotion_analyze'),
    path('biclassifyemotion/', views.biclassifyemotion, name='biclassifyemotion'),
    path('setemotion/', views.setemotion, name='setemotion'),
    path('classifytext/', views.classifytext, name='classifytext'),
    path('emotionevaluate/', views.emotionevaluate, name='emotionevaluate'),
    path('setspeech/', views.setspeech, name='setspeech'),
    path('register/', views.register, name='register'),
    path('calculate/', views.calculate, name='calculate'),
    path('index/', views.index, name='index'),
    path('user_stat/', views.user_stat, name='user_stat'),
    path('getopinion/', views.getopinion, name='getopinion'),
    path('mingxiang_stat/', views.mingxiang_stat, name='mingxiang_stat'),
    path('daysrecord/', views.daysrecord, name='daysrecord'),
    path('paper_list/', views.paper_list, name='paper_list'),
    path('mingxiang_list/', views.mingxiang_list, name='mingxiang_list'),
    path('dailyrecommend/', views.dailyrecommend, name='dailyrecommend'),
    path('getwordcloud/', views.getwordcloud, name='getwordcloud'),
    path('settestgrade/', views.settestgrade, name='settestgrade'),
    path('gettestgrade/', views.gettestgrade, name='gettestgrade'),
    path('getresume/', views.getresume, name='getresume'),
    path('gethashuserid/', views.gethashuserid, name='gethashuserid'),
    path('setopinion2/', views.setopinion2, name='setopinion2'),
    path('getopinion2/', views.getopinion2, name='getopinion2'),

#    path('chat/', views.chat, name='chat'),
]
