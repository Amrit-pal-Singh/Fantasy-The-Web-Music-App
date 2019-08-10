from music.models import Albums, Songs
from .forms import UserForms, AlbumForms, SongsForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,  logout
from django.http import HttpResponse
from django.db.models import Q


def album_list(request):
    if not request.user.is_authenticated():
        return redirect('MyMusic:login')
    all_albums = Albums.objects.all()
    all_songs = Songs.objects.all()
    query = request.GET.get("search_element")
    if query:
        albums = all_albums.filter(Q(album_name__icontains=query) | Q(artist__icontains=query)).distinct()
        song = all_songs.filter(Q(song_name__icontains=query))
        if not albums and not song:
            return render(request, 'music/index.html', {'error_message': 'No element to show'})
        return render(request, 'music/index.html', {'all_albums': albums, 'songs': song})
    return render(request, 'music/index.html', {'all_albums': all_albums})


def detail_page(request, album_id):
    if not request.user.is_authenticated():
        return redirect('MyMusic:login')
    else:
        template_name = "music/detail.html"
        albums = Albums.objects.get(id=album_id)
        return render(request, template_name, {'albums': albums})


def create_album(request):
    if not request.user.is_authenticated():
        return redirect('MyMusic:login')
    form = AlbumForms(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()
            return render(request, 'music/detail.html', {'albums': album})

    return render(request, 'music/albums_form.html', {'form': form})


def create_songs(request, pk):
    album = get_object_or_404(Albums, pk=pk)
    if not request.user.is_authenticated():
        return redirect('MyMusic:login')
    form = SongsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        song = form.save(commit=False)
        song.song_album = album
        song.song_logo = album.album_logo
        song.artist = album.artist
        song.user = request.user
        song.audio = request.FILES['audio']
        song.save()
        return render(request, 'music/detail.html', {'albums': album})
    return render(request, 'music/songs_form.html', {'form': form})
"""


def create_songs(request, pk):
    form = SongsForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Albums, pk=pk)
    if form.is_valid():
        song = form.save(commit=False)
        song.song_album = album
        song.audio = request.FILES['audio']
        song.save()
        return render(request, 'music/detail.html', {'albums': album})
    context = {
        'form': form,
    }
    return render(request, 'music/songs_form.html', context)
"""


def update_albums(request, pk):
    album = get_object_or_404(Albums, id=pk)
    if request.method == "POST":
        form = AlbumForms(request.POST, request.FILES, instance=album)
        if form.is_valid():
            album = form.save()
            album.user = request.user
            album.save()
            return render(request, 'music/detail.html', {'albums': album})
    form = AlbumForms(instance=album)
    context = {'form': form}
    return render(request, 'music/albums_form.html', context)



"""
class DeleteAlbums(DeleteView):
    model = Albums
    success_url = reverse_lazy('MyMusic:index')
"""


def delete_albums(request, album_id):
    album = Albums.objects.get(pk=album_id)
    album.delete()
    return render(request, 'music/index.html', {'all_albums': Albums.objects.all()})


def register(request):
    form = UserForms(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password, email=email)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    albums = Albums.objects.all()
                    return render(request, 'music/index.html', {'all_albums': albums})
    return render(request, 'music/register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # albums = Albums.objects.filter(user=request.user)
                # return render(request, 'music/index.html', {'all_albums': albums})
                context = {
                    'username': request.user.username,
                    'email': request.user.email,
                }
                return render(request, 'music/profile_albums.html', context)
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def logout_user(request):
    logout(request)
    return redirect('MyMusic:login')


def delete_song(request, song_id):

    song = Songs.objects.get(id=song_id)
    song.delete()
    user_album = Albums.objects.filter(user=request.user)
    song_id = []
    i = 0
    for album in user_album:
        for song in album.songs_set.all():
            song_id[i] = song.id
            i = i + 1
    users_songs = Songs.objects.filter(pk__in=song_id)

    return render(request, 'music/songs.html', {'songs': users_songs})


def songs(request):
    albums = Albums.objects.all()
    if not request.user.is_authenticated():
        return redirect('MyMusic:login')
    return render(request, 'music/songs.html', {'albums': albums})


def profile_songs(request):
    if not request.user.is_authenticated():
        return redirect('MyMusic:login')
    user_album = Albums.objects.filter(user=request.user)
    song_id = []
    i = 0
    for album in user_album:
        for song in album.songs_set.all():
            song_id.append(song.id)
    users_songs = Songs.objects.filter(pk__in=song_id)

    context = {
        'all_albums': user_album,
        'songs': users_songs,
        'username': request.user.username,
        'email': request.user.email,
    }
    return render(request, 'music/profile_songs.html', context)


def profile_albums(request):
    if not request.user.is_authenticated():
        return redirect('MyMusic:login')
    user_album = Albums.objects.filter(user=request.user)
    context = {
        'all_albums': user_album,
        'username': request.user.username,
        'email': request.user.email,
    }
    return render(request, 'music/profile_albums.html', context)


def profile(request):
    if not request.user.is_authenticated():
        return redirect('MyMusic:login')
    context = {
        'username': request.user.username,
        'email': request.user.email,
    }
    return render(request, 'music/profile_name_and_id.html', context)
