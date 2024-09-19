from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User,Post, Follow, Like
from django.contrib.auth.decorators import login_required



def index(request):
     posts= Post.objects.all().order_by("id").reverse()
     if request.user.is_authenticated:
          for post in posts:
              post.is_liked = post.post_like.filter(user=request.user).exists()
     else:
          for post in posts:
              post.is_liked = False
     paginator = Paginator(posts, 10)
     numberPage = request.GET.get('page')
     pagePosts = paginator.get_page(numberPage)
     return render(request, "network/index.html", {
     "posts" : posts,
     "pagePosts" : pagePosts
    })

@login_required
def addLike(request,postId):
        post = Post.objects.get(pk= postId)
        if not Like.objects.filter(user=request.user, post=post).exists():
                likedPost = Like(user=request.user, post=post)
                likedPost.save()

        like_count = post.post_like.count()
        return JsonResponse({"message": "Successfully added", "likedCount": like_count})

@login_required
def removeLike (request, postId):
        post = Post.objects.get(pk= postId)
        if Like.objects.filter(user=request.user, post=post).exists():
             unlikedPost = Like.objects.get(user=request.user, post=post)
             unlikedPost.delete()
        like_count = post.post_like.count()
        return JsonResponse({"message": "Successfully removed", "likedCount": like_count})

@login_required
def edit(request, postId):
    if request.method == "POST":
        data= json.loads(request.body)
        editedPost = Post.objects.get(pk= postId)
        editContent = data["content"]
        editedPost.content =editContent
        editedPost.save()
        return JsonResponse({"message": "Success", "data":data["content"]})

@login_required
def follow (request):
           user_follow = request.POST["follow"]
           user_followed = User.objects.get(username = user_follow)
           f= Follow(user = user_followed, user_follower=request.user)
           f.save()
           return HttpResponseRedirect(reverse('profile', kwargs={'id': user_followed.id}))

@login_required
def unfollow (request):
    user_unfollow = request.POST['unfollow']
    user_unfollowed = User.objects.get(username = user_unfollow)
    current_user=User.objects.get(pk= request.user.id)
    f= Follow.objects.get(user = user_unfollowed, user_follower=current_user)
    f.delete()
    return HttpResponseRedirect(reverse('profile', kwargs={'id': user_unfollowed.id}))

@login_required
def following (request):
      followings = Follow.objects.filter(user_follower = request.user)
      posts= Post.objects.all().order_by("id").reverse()
      for post in posts:
                 post.is_liked = post.post_like.filter(user=request.user).exists()
      followingPosts = []
      for post in posts:
        for person in followings:
            if person.user == post.author:
                followingPosts.append(post)
      paginator = Paginator(followingPosts, 10)
      numberPage = request.GET.get('page')
      pagePosts = paginator.get_page(numberPage)
      return render(request, "network/following.html", {
     "posts" : followingPosts,
     "pagePosts" : pagePosts
    })

def profile(request, id):
     user = User.objects.get(pk = id)
     posts= Post.objects.filter(author = user).order_by("id").reverse()
     for post in posts:
         post.is_liked = post.post_like.filter(user=request.user).exists()
     followers = Follow.objects.filter(user = user)
     followings = Follow.objects.filter(user_follower= user)
     paginator = Paginator(posts, 10)
     numberPage = request.GET.get('page')
     pagePosts = paginator.get_page(numberPage)
     if request.user.is_authenticated:
         user_follower = followers.filter(user_follower= request.user)
         if len(user_follower) != 0:
            is_following = True
         else:
            is_following = False
     else:
            is_following = False
     return render(request, "network/profile.html", {
      "username" : user.username,
       "posts" : posts,
      "pagePosts" : pagePosts,
      "followers" : followers ,
      "followings" : followings,
      "user_profile" : user,
      "is_following" : is_following
                })

@login_required
def addPost(request):
    if request.method =="POST":
        content = request.POST['newPost']
        user = request.user
        newPost =Post(content= content, author = user)
        newPost.save()
        return HttpResponseRedirect(reverse('index'))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
