from django.db import models
from django.contrib.auth.models import User


class Albums(models.Model):
    user = models.ForeignKey(User, default=1)
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField(default='images/music-icons-gold-692289-39811.png', upload_to='images')

    def __str__(self):
        return self.album_name


class Songs(models.Model):
    song_name = models.CharField(max_length=100)
    song_album = models.ForeignKey(Albums, on_delete=models.CASCADE)
    song_logo = models.FileField(default='images/music_icon.png', upload_to='images')
    artist = models.CharField(max_length=100, default="unknown")
    audio = models.FileField(upload_to='songs', default="")

    def __str__(self):
        return self.song_name














