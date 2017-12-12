from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^allGames/$', views.AllGames.as_view(), name='allGames'),
    url(r'^$', views.UserFormView.as_view(), name='registration'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^favourite/$', views.Favourite.as_view(), name='favourite'),
    url(r'^autocomplete/$', views.AutoComplete.as_view(), name='autocomplete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
