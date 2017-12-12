from .models import Game,Favourites
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GameSerializer


class AllGames(generic.DetailView):
    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('registration')
        games = Game.objects.all()
        query = request.GET.get("q")
        platform_list = request.GET.getlist('platforms')
        platforms = games.values("platform").distinct()
        if query:
            games = games.filter(
                Q(title__icontains=query)
            ).distinct()
        sort = request.GET.get("score")
        if sort == 'asc':
            games = games.order_by('score')
        else:
            games = games.order_by('-score')
        if platform_list:
            games = games.filter(platform__in=platform_list)

        page = request.GET.get('page', 1)
        paginator = Paginator(games, 12)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)

        fav_list = Favourites.objects.filter(user=request.user.id).values_list('game', flat=True)
        if query or sort or platform_list:
            return render(request,
                          'gameSearch/SearchResults.html',
                          {'games': games, 'user': request.user, 'platforms': platforms,
                           'platform_filter': platform_list, 'favourites': fav_list})
        else:
            return render(request,
                          'gameSearch/GameList.html',
                          {'games': games, 'user': request.user, 'platforms': platforms,
                           'platform_filter': platform_list, 'favourites': fav_list})


class UserFormView(View):
    form_class = UserForm
    template_name = 'gameSearch/registration.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('allGames')
        else:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('allGames')

        return render(request, self.template_name, {'form': form})


class Login(View):

    template_name = 'gameSearch/registration.html'

    def get(self, request):
        return redirect('registration')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('allGames')
            else:
                return render(request, self.template_name, {'error_message': 'Your account has been disabled'})
        else:
            return render(request, self.template_name, {'error_message': 'Credentials did not match'})
        return render(request, self.template_name)


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('registration')


class AutoComplete(APIView):

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('registration')
        games = Game.objects.all()
        titles = games.values('title').distinct()
        query = request.GET.get("search")
        titles = titles.filter(
            Q(title__istartswith=query)
        ).distinct()
        serializer = GameSerializer(titles, many=True)
        return Response(serializer.data)


class Favourite(View):

    template_name = 'gameSearch/GameList.html'

    def post(self, request):
        id = request.POST['id']
        user_id = str(request.user.id)
        games = Game.objects.all()
        selected_game = games.get(id=id).id
        favourite = Favourites(user=user_id, game=selected_game)
        favourite.save()
        return HttpResponse(selected_game)
