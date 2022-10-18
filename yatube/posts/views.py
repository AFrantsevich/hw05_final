from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User, Follow
from .utilits import paginator_func
from .forms import PostForm, CommentForm


NUMB_POSTS = 10


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    page_obj = paginator_func(request, post_list, NUMB_POSTS)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.filter(group=group)
    page_obj = paginator_func(request, posts, NUMB_POSTS)
    context = {'group': group, 'page_obj': page_obj}
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author)
    page_obj = paginator_func(request, post_list, NUMB_POSTS)
    following = False
    if request.user.is_authenticated and request.user != author:
        following = author.following.filter(user=request.user,
                                            author=author).exists()

    context = {'author': author,
               'page_obj': page_obj, 'following': following
               }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    form = CommentForm(request.POST or None, )
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create.html'
    form = PostForm(request.POST, files=request.FILES or None,)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.text = form.cleaned_data['text']
        new_post.group = form.cleaned_data['group']
        new_post.author = request.user
        new_post.save()
        return redirect('posts:profile', new_post.author)
    context = {'form': form}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create.html'
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        if request.method == "POST":
            form = PostForm(request.POST or None,
                            files=request.FILES or None,
                            instance=post)
            if form.is_valid():
                form.text = form.cleaned_data['text']
                form.group = form.cleaned_data['group']
                form.save()
                return redirect('posts:post_detail', post_id)
        form = PostForm(instance=post)
        return render(request,
                      template,
                      {'form': form, 'is_edit': True})
    return redirect('posts:post_detail', post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None,)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    post_list = Post.objects.filter(author__following__user=request.user)
    page_obj = paginator_func(request, post_list, NUMB_POSTS)
    context = {'page_obj': page_obj}
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        if not author.following.filter(
                user=request.user, author=author).exists():
            follower = Follow()
            user = get_object_or_404(User, username=request.user)
            author = get_object_or_404(User, username=username)
            follower.author = author
            follower.user = user
            follower.save()
            return redirect('posts:profile', username)
    return redirect('posts:main')


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follower = Follow.objects.filter(
        user=request.user).filter(author=author)
    if follower:
        follower.delete()
    return redirect('posts:profile', username)
