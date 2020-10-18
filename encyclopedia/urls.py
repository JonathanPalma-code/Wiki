from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.subject, name="subject"),
    path("search/", views.search, name="search"),
]
