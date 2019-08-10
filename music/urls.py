from django.conf.urls import url
from . import views
app_name = "MyMusic"
# r is regular expression


urlpatterns = [
    url(r'^index/$', views.album_list, name="index"),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail_page, name="details"),
    url(r'^albums/add/$', views.create_album, name="add-albums"),
    url(r'^albums/(?P<pk>[0-9]+)/add/$', views.create_songs, name="add-songs"),
    url(r'^albums/(?P<album_id>[0-9]+)/delete_albums/$', views.delete_albums, name="delete_Albums"),
    url(r'^albums/delete_song/(?P<song_id>[0-9]+)', views.delete_song, name='delete_song'),
    url(r'^albums/(?P<pk>[0-9]+)/$', views.update_albums, name="update-albums"),
    url(r'^login/$', views.login_user, name="login"),
    url(r'^songs/', views.songs, name='songs'),
    url(r'^register/$', views.register, name="register"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^profile/Songs', views.profile_songs, name="profile_songs"),
    url(r'^profile/albums', views.profile_albums, name="profile_albums")
]








