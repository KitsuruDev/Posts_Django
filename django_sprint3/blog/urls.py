from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.all_posts, name='all_posts'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment/', views.comment_add, name='comment_add'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
]