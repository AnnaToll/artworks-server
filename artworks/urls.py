from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home),
    path("om-mig", views.about),
    path("kontakt", views.contact),
    path("categories", views.categories),
    path("nav", views.nav, name="nav"),
    path("art/<str:category_id>", views.art),
    path("login", views.login),
    path("logout", views.logout),
    path("authenticate", views.check_authentication),
]