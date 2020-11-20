from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addUser', views.addUser),
    path('userPage', views.userPage),
    path('destroySession', views.destroySession),
    path('loginUser', views.loginUser)
]
