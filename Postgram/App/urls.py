from base64 import urlsafe_b64decode
from django import urls
from django.urls import path
from . import views
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth.models import UserManager


urlpatterns = [
    path('', views.index,name = 'index'),
    path('createprofile/', views.create_profile,name="signUp"),
    path('login/',views.Login,name="Login"),
    path('logout/',views.logout,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('search/',views.search,name='search'),
    path('follow/<int:id>/<str:username>/',views.follow,name = "follow"),
    path('uploadpost/',views.upload_post,name="upload_post"),
    path('like/<int:id>/',views.like_post,name="like"),
    path("upload_reel",views.upload_reel,name="upload_reel"),
    path('reels/',views.reels,name="reels"),
    path("likereel/<int:id>/",views.like_reel,name="likereel"),
    path("uploadstory/",views.upload_story,name="upload_story"),
]

