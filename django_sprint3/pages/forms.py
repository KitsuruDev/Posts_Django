from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, label="Ник")
    first_name = forms.CharField(max_length=150, required=True, label="Имя")
    last_name = forms.CharField(max_length=150, required=True, label="Фамилия")
    email = forms.EmailField(required=True, label="Почта")

    class Meta:
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")

class ProfileEditForm(UserChangeForm):
    username = forms.CharField(max_length=150, required=True, label="Ник")
    first_name = forms.CharField(max_length=150, required=True, label="Имя")
    last_name = forms.CharField(max_length=150, required=True, label="Фамилия")
    email = forms.EmailField(required=True, label="Почта")

    class Meta(UserChangeForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password", None)

class CustomPasswordChangeForm(PasswordChangeForm):
    pass