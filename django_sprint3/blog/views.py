from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment
from .forms import PostCreateForm, CommentForm
from django.utils import timezone


def paginate(request, objects):
    paginator = Paginator(objects, 10)
    page = request.GET.get('page')
    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)
    return paginated_objects


def index(request):
    posts = Post.objects.filter(is_published=True, category__is_published=True,
                                published_date__lte=timezone.now()).order_by('-published_date')
    paginated_posts = paginate(request, posts)
    return render(request, 'index.html', {'posts': paginated_posts})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    posts = Post.objects.filter(category=category, is_published=True,
                                published_date__lte=timezone.now()).order_by('-published_date')
    paginated_posts = paginate(request, posts)
    return render(request, 'category.html', {'category': category, 'posts': paginated_posts})


def all_posts(request):
    posts = Post.objects.filter(is_published=True, category__is_published=True,
                                published_date__lte=timezone.now()).order_by('-published_date')
    paginated_posts = paginate(request, posts)
    return render(request, 'category.html', {'posts': paginated_posts, 'category': None, 'user': request.user})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comment_form': comment_form})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('pages:profile', kwargs={'username': request.user.username}))
    else:
        form = PostCreateForm()
    return render(request, 'post_create.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect('blog:post_detail', pk=pk)

    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostCreateForm(instance=post)

    return render(request, 'post_create.html', {'form': form, 'post': post})


@login_required
def comment_add(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_add.html', {'form': form, 'post': post})

@login_required
def comment_edit(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if comment.author != request.user:
        return redirect('blog:post_detail', pk=post.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comment_edit.html', {'form': form, 'post': post, 'comment': comment})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect('blog:post_detail', pk=post.pk)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:all_posts')

    return render(request, 'post_detail.html', {'post': post, 'confirm_delete': True})


@login_required
def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if comment.author != request.user:
        return redirect('blog:post_detail', pk=post.pk)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk=post.pk)

    return render(request, 'comment_edit.html', {'post': post, 'comment': comment, 'confirm_delete': True})