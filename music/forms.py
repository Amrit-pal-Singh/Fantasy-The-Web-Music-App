from django.contrib.auth.models import User
from django import forms
from music.models import Albums, Songs


class UserForms(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AlbumForms(forms.ModelForm):
    class Meta:
        model = Albums
        fields = ["album_name", "artist", "genre", "album_logo"]


class SongsForm(forms.ModelForm):
    class Meta:
        model = Songs
        fields = ['song_name', 'audio']

















