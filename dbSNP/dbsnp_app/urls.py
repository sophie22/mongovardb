from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	path("", views.home, name="home"),
	path("home/", views.home, name="home"),
	path("results/", views.results, name="results"),
	path("help/", views.help, name="help"),


]

urlpatterns += staticfiles_urlpatterns()