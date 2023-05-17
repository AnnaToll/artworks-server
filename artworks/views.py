from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict

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