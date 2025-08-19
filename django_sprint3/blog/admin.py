# blog/admin.py
from django.contrib import admin
from .models import Category, Location, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published',)
    search_fields = ('title', 'description')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('author', 'category', 'location', 'is_published')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    filter_horizontal = ()
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'author', 'published_date', 'is_published', 'category', 'location')
        }),
    )