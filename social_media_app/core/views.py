from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from . import models

# Create your views here.
@login_required(login_url='login/')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = models.Profile.objects.get(user=user_object)
    posts =models.Post.objects.all()
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts, 'username': request.user.username})

@login_required(login_url='login/')
def like(request, postid):
    post_id = postid
    post = models.Post.objects.get(id=post_id)
    likePost = models.LikePost.objects.filter(post=post, user=request.user)
    if likePost.exists():
        likePost.delete()
        post.no_likes = post.no_likes -1
        post.save()
    else:
        new_like = models.LikePost.objects.create(post=post, user=request.user)
        new_like.save()
        post.no_likes = post.no_likes + 1
        post.save()
    return redirect('/')

@login_required(login_url='login/')
def upload(request):
    if request.method == 'POST':
        user_object = User.objects.get(username=request.user.username)
        image = request.FILES.get('upload_image')
        caption = request.POST['caption']
        new_post = models.Post.objects.create(user=user_object, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    return redirect('/')

@login_required(login_url='login/')
def profile(request, username):
    user = User.objects.get(username=username)
    current_user = user == request.user
    profile = models.Profile.objects.get(user=user)
    posts = models.Post.objects.filter(user=user)
    follower_count = len(models.FollowerCount.objects.filter(user=user))
    following_count = len(models.FollowerCount.objects.filter(follower=user)) 
    
    if models.FollowerCount.objects.filter(user=user, follower=request.user).exists():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    num_posts = len(posts)
    context = {
        "current_user": current_user,
        "user": user,
        "profile": profile,
        "posts": posts,
        "num_posts": num_posts,
        'follower_count': follower_count,
        'following_count': following_count,
        'button_text': button_text,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login/')
def follow(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['user'])
        follower = models.FollowerCount.objects.filter(user=user, follower=request.user)
        if follower.exists():
            follower.delete()
        else:
            new_follower = models.FollowerCount.objects.create(user=user, follower=request.user)
            new_follower.save()
        return redirect(f'/profile/{user.username}')
    return redirect('/')

@login_required(login_url='login/')
def settings(request):
    user_profile = models.Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_profile.bio = request.POST['bio']
        if request.FILES.get('image') != None:
            user_profile.profile_img = request.FILES.get('image')
        user_profile.save()
    return render(request, 'settings.html', {'user_file': user_profile})

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            error = 'Passwords do not match'
            return render(request, 'signup.html', {'error_message': error})
        if models.User.objects.filter(username=username).exists():
            error = 'Username is already taken'
            return render(request, 'signup.html', {'error_message': error})
        if models.User.objects.filter(email=email).exists():
            error = 'Email is already taken'
            return render(request, 'signup.html', {'error message': error})
        try:
            new_user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
            new_user.save()
            new_profile = models.Profile.objects.create(user=new_user, id_user=new_user.id)
            new_profile.save()
            auth.login(new_user)
            return redirect('home')
        except: 
            error = 'Error during User creation'
            return render(request, 'signup.html', {'error_message': error})
    return render(request, 'signup.html')
    
def login(request):
    if request.method == "POST": 
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        error = 'Invalid username and/or password'
        return render(request, 'login.html', {'error_message': error})
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')