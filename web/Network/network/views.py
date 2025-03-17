import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages

from .models import User, Post, Follow, Like


def index(request):
    posts = Post.objects.all().order_by("-created_date")
    posts_page, page_range = get_posts_with_pagination(request, posts)
    return render(request, "network/index.html", {
        "posts": posts_page,
        "posts_page_range": page_range
    })


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


@login_required
def new_post(request):
    if request.method != "POST":
        messages.error(request, "Bad request")
        return HttpResponseRedirect(reverse("index"))

    post = Post(content=request.POST.get("content", ""), user=request.user)
    
    # check if post is valid and post is not (nearly) same content
    if not post.is_valid() or Post.objects.filter(content__contains=post.content).count() != 0:
        messages.error(
            request, "Can not create post because post's content is blank or post's content is the (nearly) same with another")
        return HttpResponseRedirect(reverse("index"))

    post.save()

    return HttpResponseRedirect(reverse("index"))


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by("-created_date")
    # toggle button logic
    is_following = True if Follow.objects.filter(
        user=user, follower=request.user).exists() else False

    # get all post with pagination
    posts_page, page_range = get_posts_with_pagination(request, posts)
    return render(request, "network/profile.html", {
        "count_people_follow_profile_user": Follow.objects.filter(user=user).count(),
        "count_people_profile_user_follows": Follow.objects.filter(follower=user).count(),
        "posts": posts_page,
        "posts_page_range": page_range,
        "profile_user": user,
        "follow": is_following
    })


@login_required
def follow(request):
    username = json.loads(request.body)["user"]

    if request.method != "POST" or username is None or username == request.user.username:
        messages.error(request, "Bad request")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    # try to get user given username
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "Profile does not exist")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    # try to remove follow of profile user of request user if follow is in table, vice versa
    try:
        Follow.objects.get(user=user, follower=request.user).delete()
        toggle_follow_btn = False
    except Follow.DoesNotExist:
        Follow.objects.create(user=user, follower=request.user)
        toggle_follow_btn = True

    return JsonResponse({"toggle_follow_btn": toggle_follow_btn,
                         "count_people_follow_profile_user": Follow.objects.filter(user=user).count(),
                         "count_people_profile_user_follows": Follow.objects.filter(follower=user).count()}, status=200)


@login_required
def like(request, post_id):
    if request.method != "POST":
        messages.error(request, "Bad request")
        return HttpResponseRedirect(reverse("index"))

    # try to get post with id
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        messages.error(request, "Post does not exist")
        return HttpResponseRedirect(reverse("index"))

    # try to remove like of current post of request user if like is in table, vice versa
    try:
        Like.objects.get(user=request.user, post=post).delete()
        like_post = False
    except Like.DoesNotExist:
        Like.objects.create(user=request.user, post=post)
        like_post = True

    # get all likes from current post
    count_likes = Like.objects.filter(post=post).count()
    return JsonResponse({"like_post": like_post, "count_likes": count_likes}, status=200)


@login_required
def edit(request, post_id):
    # get post which belongs to owner if current user is post's owner
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=400)

    if request.user != post.user:
        return JsonResponse({"error": "You are not allow to edit this post"}, status=400)

    # get edit page
    if request.method == "GET":
        return render(request, "network/edit.html", {
            'post': post
        })

    if request.method != "POST":
        messages.error(request, "Bad request")
        return HttpResponseRedirect(reverse("index"))

    # update content of post if content not empty and not exist in db
    content = json.loads(request.body)["content"]
    if content == "":
        return JsonResponse({"error": "Post's content can not be blank"}, status=400)
    elif Post.objects.filter(content__contains=content).count() != 0:
        return JsonResponse({"error": "Update content is the (nearly) same with Post's content"}, status=400)

    post.content = content
    post.save()
    return JsonResponse({"success": "Update post successful"}, status=200)


@login_required
def following_posts(request):
    # get all users who are followed by request user
    users = Follow.objects.filter(follower=request.user)

    # get posts for each users above
    posts = Post.objects.none()
    for user in users:
        posts |= Post.objects.filter(user=user.user)
    posts = posts.order_by("-created_date")
    posts_page, page_range = get_posts_with_pagination(request, posts)
    return render(request, "network/index.html", {
        "posts": posts_page,
        "posts_page_range": page_range,
        "following": True
    })


def get_posts_with_pagination(request, posts):
    page_number = request.GET.get('page', 1)
    posts_obj = []
    for post in posts:
        like_post = None
        # get like of each post for user signed in
        if request.user.is_authenticated:
            if Like.objects.filter(user=request.user, post=post).exists():
                like_post = True
            else:
                like_post = False
        else:
            like_post = None

        # get likes count for current post
        count_likes = Like.objects.filter(post=post).count()
        posts_obj.append([post, like_post, count_likes])

    # 10 posts per page
    paginator = Paginator(posts_obj, 10)
    # get posts based on page number, default page is 1
    posts_page = paginator.get_page(page_number)

    margin = 2
    # Get the index of the current page
    current_index = posts_page.number - 1

    # This value is maximum index of pages, so the last page - 1
    max_index = len(paginator.page_range)
    # Calculate left page range based on margin at current index
    start_index = current_index - margin if current_index >= margin else 0
    # Calculate right page range based on margin at current index
    end_index = current_index + margin + \
        1 if current_index <= max_index - margin - 1 else max_index
    # Get new page range
    page_range = list(paginator.page_range)[start_index:end_index]
    return (posts_page, page_range)
