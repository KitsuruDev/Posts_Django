from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.template import loader
from .forms import RegistrationForm, ProfileEditForm, CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

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


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = 'Добро пожаловать на наш сайт!'
            message = f'Привет, {user.username}!\n\nСпасибо за регистрацию!'
            from_email = 'noreply@example.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('pages:profile', kwargs={'username': username}))
            else:
                form.add_error(None, "Неверное имя пользователя или пароль")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post_set.all().order_by('-published_date')
    paginated_posts = paginate(request, posts)
    return render(request, 'accounts/profile.html', {'user': user, 'posts': paginated_posts})


def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('pages:profile', username=username)
    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


def change_password(request, username):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('pages:profile', username=username)
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


def about(request):
    about_text = """
    Наш проект посвящен сбору и публикациям ваших историй.
    """
    return render(request, 'about.html', {'text': about_text, 'title': "О проекте"})


def rules(request):
    rules_text = """
    1. Запрещается размещать контент, нарушающий моральные законы!
    2. Будьте вежливы!
    3. Не спамьте и ничего не рекламируйте!
    """
    return render(request, 'rules.html', {'text': rules_text, 'title': "Наши правила"})


def handler403(request, exception=None):
    return render(request, '403.html', status=403)

def handler404(request, exception=None):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def csrf_failure(request, reason=""):
    template = loader.get_template('csrf_failure.html')
    return HttpResponseForbidden(template.render(request=request))