from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json


from .models import User, Category, Artwork, Page

def artist_as_json(request):
    artist = User.models.find(User=request.user)
    return JsonResponse({ "artist": artist })


def to_response_list(query_set):
    return { "success": list(query_set.values()) }


def home(request):
    page = Page.objects.get(page="Start")
    categories = Category.objects.filter(page=page).order_by("priority")
    return JsonResponse(to_response_list(categories))


def nav(request):
    page = Page.objects.filter(navigation_order__gt=0).values()
    category = Category.objects.filter(navigation_order__gt=0).values()
    nav = list(page) + list(category)
    sorted_nav = sorted(nav, key=lambda nav_item : nav_item['navigation_order'])
    return JsonResponse({ "success": sorted_nav })


def about(request):
    return artist_as_json(request)


def contact(request):
    return artist_as_json(request)


def categories(request):
    pass


def art(request, category_id):
    category = Category.objects.get(id=category_id)
    art = Artwork.objects.filter(category=category)
    return JsonResponse(to_response_list(art))


def check_authentication(request):
    is_authenticated = request.user.is_authenticated
    return JsonResponse({ "success": { "isAuthenticated": is_authenticated }})


@csrf_exempt
def logout(request):
    auth_logout(request)
    return JsonResponse({ "success": "You have successfully been logged out."})


@csrf_exempt
def login(request):
    if request.method == "POST":
        req = json.loads(request.body)
        error = ""
        email = req["email"]
        password = req["pwd"]
        email_exists = User.objects.filter(email=email).exists()
        user = None
        if not email_exists:
            error = "Email is not registered."
        else:
            user = authenticate(request, username=email, password=password)
            if user is None:
                error = "Email and password does not match."

        if user is not None:
            response = JsonResponse({ "success": { "name": getattr(user, "first_name"), "email": getattr(user, "email") } })
            # auth_login(request, user)
            # get_token(request)
            response.set_cookie("Test", "Please work", samesite="None", secure=True, httponly=False)
            return response
        else:
            return JsonResponse({ "error": error}, status=401)