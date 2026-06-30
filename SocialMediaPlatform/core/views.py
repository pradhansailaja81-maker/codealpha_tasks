from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Post
from .forms import ProfileForm
from .models import Like
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Comment
from .forms import CommentForm
from .models import Follow


def home(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", {"posts": posts})


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()

    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("home")

    else:
        form = PostForm()

    return render(request, "create_post.html", {"form": form})


@login_required
def profile(request, username):

    profile_user = get_object_or_404(User, username=username)

    profile = profile_user.profile

    posts = Post.objects.filter(user=profile_user)

    followers = Follow.objects.filter(
        following=profile_user
    ).count()

    following = Follow.objects.filter(
        follower=profile_user
    ).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    context = {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "followers": followers,
        "following": following,
        "is_following": is_following,
    }

    return render(request, "profile.html", context)


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)

    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = PostForm(instance=post)

    return render(request, "edit_post.html", {"form": form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)

    if request.method == "POST":
        post.delete()
        return redirect("home")

    return render(request, "delete_post.html", {"post": post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)

    return redirect("home")

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

    return redirect("home")



def search_users(request):
    query = request.GET.get("q")
    users = []

    if query:
        users = User.objects.filter(username__icontains=query)

    return render(request, "search.html", {
        "query": query,
        "users": users,
    })

@login_required
def follow_user(request, username):
    profile_user = get_object_or_404(User, username=username)

    if profile_user != request.user:
        Follow.objects.get_or_create(
            follower=request.user,
            following=profile_user
        )

    return redirect("profile", username=username)


@login_required
def unfollow_user(request, username):
    profile_user = get_object_or_404(User, username=username)

    Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).delete()

    return redirect("profile", username=username)