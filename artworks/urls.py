from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home),
    path("om-mig", views.about),
    path("kontakt", views.contact),
    path("categories", views.categories),
    path("images", views.images),
    path("category/<str:category_id>", views.category),
    path("nav", views.nav, name="nav"),
    path("art/<str:category_id>", views.art),
    path("artworks", views.artworks),
    path("artwork/<str:art_id>", views.artwork),
    path("login", views.login),
    path("logout", views.logout),
    path("pages", views.pages),
    path("page/<str:page_id>", views.page),
    path("all", views.all),
    path("authenticate", views.check_authentication),
]