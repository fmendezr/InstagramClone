from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.serializers import serialize
from . import models

# Create your views here.
@login_required(login_url='login/')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = models.Profile.objects.get(user=user_object)

    user_following = [user.user for user in models.FollowerCount.objects.filter(follower=user_object)]
    posts = models.Post.objects.filter(user__in=user_following).order_by('-created')

    suggested_users = models.Profile.objects.exclude(user__in=user_following).exclude(user=user_object)
    size_s_u = len(suggested_users)
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts, 'username': request.user.username, 'suggested_users': suggested_users[: 5 if size_s_u >= 5 else size_s_u]})

@login_required(login_url='login/')
def like(request, postid):
    post_id = postid
    post = models.Post.objects.get(id=post_id)
    likePost = models.LikePost.objects.filter(post=post, user=request.user)
    if likePost.exists():
        likePost.delete()
        post.no_likes = post.no_likes -1
        post.save()
        return JsonResponse({'action' : 'unliked', 'n_likes': post.no_likes})
    else:
        new_like = models.LikePost.objects.create(post=post, user=request.user)
        new_like.save()
        post.no_likes = post.no_likes + 1
        post.save()
        return JsonResponse({'action' : 'liked', 'n_likes': post.no_likes})

@login_required(login_url='login')
def is_liked(request, postid):
    if models.LikePost.objects.filter(post__id=postid, user=request.user).exists():
        return JsonResponse({'liked': "yes"})
    else:
        return JsonResponse({'liked': "no"})

    
@login_required(login_url='login/')
def upload(request):
    if request.method == 'POST':
        user_object = User.objects.get(username=request.user.username)
        image = request.FILES.get('upload_image')
        caption = request.POST['caption']
        new_post = models.Post.objects.create(user=user_object, image=image, caption=caption)
        new_post.save()
        return redirect(f'/profile/{request.user.username}')
    return redirect('/')

@login_required(login_url='login/')
def search(request):
    profile = models.Profile.objects.get(user=request.user)
    context = {'user_profile': profile, 'username': request.user.username}
    if request.method == 'POST':
        username = request.POST['user_search']
        user_results = User.objects.filter(username__contains=username)
        user_list = [ user for user in user_results]
        profile_results = models.Profile.objects.filter(user__in=user_list)
        context['profiles_found'] = profile_results
        return render(request, 'search.html', context)
    return render(request, 'search.html', context)

@login_required(login_url='login/')
def profile(request, username):
    user = User.objects.get(username=username)
    current_user = user == request.user
    current_profile = models.Profile.objects.get(user=request.user)
    profile = models.Profile.objects.get(user=user)
    posts = models.Post.objects.filter(user=user).order_by('-created')
    followers = models.FollowerCount.objects.filter(user=user)
    following = models.FollowerCount.objects.filter(follower=user)
    follower_count = len(followers)
    following_count = len(following) 
    
    if models.FollowerCount.objects.filter(user=user, follower=request.user).exists():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    num_posts = len(posts)
    context = {
        "username": request.user.username,
        "user_profile": current_profile,
        "current_user": current_user,
        "user": user,
        "profile": profile,
        "posts": posts,
        "num_posts": num_posts,
        'followers' : followers,
        'following': following,
        'follower_count': follower_count,
        'following_count': following_count,
        'button_text': button_text,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login/')
def follow(request, username):
    user = User.objects.get(username=username)
    follower = models.FollowerCount.objects.filter(user=user, follower=request.user)
    if follower.exists():
        follower.delete()
        return JsonResponse({'action': 'unfollow'})
    else:
        new_follower = models.FollowerCount.objects.create(user=user, follower=request.user)
        new_follower.save()
        return JsonResponse({'action': 'follow'})
    return HttpResponse(400)
   

@login_required(login_url=('login/'))
def remove(request, username):
    user = User.objects.get(username=username)
    follower = models.FollowerCount.objects.filter(user=request.user, follower=user)
    follower.delete()
    return HttpResponse(200)

@login_required(login_url='login/')
def delete_post(request, postid):
    if request.method == 'POST':
        post = models.Post.objects.get(id=postid)
        post.delete()
        return redirect(f'/profile/{request.user.username}')

@login_required(login_url='login/')
def settings(request):
    user_profile = models.Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_profile.bio = request.POST['bio']
        if request.FILES.get('image') != None:
            user_profile.profile_img = request.FILES.get('image')
        user_profile.save()
    return render(request, 'settings.html', {'user_profile': user_profile, "username": user_profile.user.username})

@login_required(login_url='login/')
def saved_posts(request):
    profile = models.Profile.objects.get(user=request.user)
    posts = models.SavePost.objects.filter(user=request.user)
    return render(request, 'saved_posts.html', {'user_profile': profile, 'username': request.user.username, 'posts': posts})

@login_required(login_url='login/')
def save(request, postid):
    post = models.Post.objects.get(id=postid)
    save_post = models.SavePost.objects.filter(post=post)
    if save_post.exists():
        save_post.delete()
        return JsonResponse({'action': 'unsaved'})
    else:
        save_post = models.SavePost.objects.create(post=post, user=request.user)
        save_post.save()
        return JsonResponse({'action': 'saved'})

@login_required(login_url='login/')
def is_saved(request, postid):
    if models.SavePost.objects.filter(post__id=postid, user=request.user).exists():
        return JsonResponse({'liked': "yes"})
    else:
        return JsonResponse({'liked': "no"})


@login_required(login_url='login/')
def comments(request, postid):
    if request.method == 'POST':
        post = models.Post.objects.get(id=postid)
        comment_text = request.POST['comment']
        comment = models.CommentPost(post=post, user=request.user, comment=comment_text)
        comment.save()
        return JsonResponse({'user': request.user.username, 'comment': comment_text})
    comments = models.CommentPost.objects.filter(post__id=postid).order_by('created')
    users_in_comments = [comment.user for comment in comments]
    data_2 = serialize('json', users_in_comments, fields=['username'])
    data = serialize('json', comments)
    return JsonResponse({'comments': data, 'users': data_2})

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
        except: 
            error = 'Error during User creation'
            return render(request, 'signup.html', {'error_message': error})
        try: 
            auth.login(request, new_user)
            return redirect('home')
        except:
            error = "Account Created Succesfully"
            return render(request, 'login.html', {'error_message': error} )
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