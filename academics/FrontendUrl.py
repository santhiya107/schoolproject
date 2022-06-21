from django.urls import path
from.FrontendViews import *


urlpatterns=[
   
    path('login',simple,name='simplelogin'),
    path('',gradeview,name='gradeview'),
    path('chapcreate',chaptercreateview,name='chaptercreateview'),
    path('subcreate',subjectcreateview,name='subcreateview'),
    # path('sublist',subjectlistview,name='sublistview'),
    path('subedit/<int:pk>/',subjectEdit,name='subjectedit'),
    path('subdelete/<int:pk>/',subjectdelete,name='subjectdelete'),
    path('chapedit/<int:pk>/',chapterEdit,name='chapteredit'),
    path('chaplist',chapterlistview,name='chapterlistview'),
    path('ques',questioncreationview,name='questioncreationview'),
    path('queslist',questionlistview,name='questionlistview'),
   
    
]