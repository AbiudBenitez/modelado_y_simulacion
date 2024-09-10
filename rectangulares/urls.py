from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("proyects/", views.proyecta),
    path("task/<int:id>", views.task),
    path("tasks/rectangulares_mixto/", views.rectangulares_mixto, name="rectangulares_mixto"),
    path("tasks/recValue/", views.recValue, name="recValue")
]
