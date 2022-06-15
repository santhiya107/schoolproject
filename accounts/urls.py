from django.urls import path
from.views import (
    SignupView,
    LoginView,
    StudentProfileView,
    UserDetailsView,
    UserDetailsEditView,
    LogoutView,
    LoginVerifyView,
    SimpleLoginView,
    ProfileView
)


urlpatterns=[
    path('signup/',SignupView.as_view()),
    path('login/',LoginView.as_view()),
    path('login-verify/',LoginVerifyView.as_view()),
    path('login2/',SimpleLoginView.as_view(),name='login_2'),
    path('logout/',LogoutView.as_view()),
    path('student-profile/<int:pk>/',StudentProfileView.as_view()),
    path('user-details/',UserDetailsView.as_view()),
    path('user-details/<int:pk>/',UserDetailsEditView.as_view()),
    path('profile/',ProfileView.as_view())
 
]