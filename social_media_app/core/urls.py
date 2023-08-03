from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('like/<str:postid>/', views.like, name='like'),
    path('is-liked/<str:postid>/', views.is_liked, name='is_liked'),
    path('upload/', views.upload, name='upload'),
    path('search/', views.search, name='search'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('remove/<str:username>/', views.remove, name='remove'),
    path('delete-post/<str:postid>', views.delete_post, name='delete_post'),
    path('saved-posts/', views.saved_posts, name='saved_posts'), 
    path('save/<str:postid>', views.save, name='save'),
    path('is-saved/<str:postid>', views.is_saved, name='is_saved'),
    path('comments/<str:postid>', views.comments, name='comments'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings')
]
