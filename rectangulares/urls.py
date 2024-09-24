from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("proyects/", views.proyecta),
    path("task/<int:id>", views.task),
    path("tasks/rectangulares_mixto/", views.rectangulares_mixto, name="rectangulares_mixto"),
    path("tasks/rectangulares_multi/", views.rectangulares_multi, name="rectangulares_multi"),
    path("tasks/rectangulares_mixto/respuesta", views.recValue, name="recValue"),
    path("tasks/rectangulares_multi/respuesta", views.recMultiValue, name="recMultiValue"),
    path("tasks/pruebas/", views.promedios, name="promedios"),
    #SE DECLARAN LOS URLS QUE SOLO PROCESAN DATOS
    path("mixtos_datos/", views.mixtos_datos, name="mixtos_datos"),
    path("multi_datos/", views.multi_datos, name="multi_datos"),
    path("calcular_alpha/", views.calcular_alpha, name="calcular_alpha"),
    path("calcular_alpha_dn/", views.calcular_alpha_dn, name="calcular_alpha_dn"),
    path("promedio_value/", views.promedio_value, name="promedio_value"),
    path("ks_value/", views.ks_value, name="ks_value"),
    path("f_value/", views.f_value, name="f_value"),
]
