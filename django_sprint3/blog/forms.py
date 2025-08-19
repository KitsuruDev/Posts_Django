from django import forms
from .models import Post, Category, Location, Comment


class PostCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_published=True),
        required=True,
        label="Категория"
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_published=True),
        required=True,
        label="Местоположение"
    )
    published_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=True,
        label="Дата и время публикации"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'location', 'image', 'published_date', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }