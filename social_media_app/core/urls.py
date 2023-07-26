from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('like/<str:postid>/', views.like, name='like'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/', views.follow, name='follow'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings')
]
