from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("om-mig", views.about, name="about"),
    path("kontakt", views.contact, name="contact"),
    path("categories", views.categories, name="categories"),
    path("nav", views.nav, name="nav"),
    path("art/<str:category_id>", views.art, name="art"),
]