from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_image",
            "bio",
            "location",
            "website",
        ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "image",
            "caption",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
        ]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "caption"]