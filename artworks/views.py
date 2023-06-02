from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json
import logging

logger = logging.getLogger("mylogger")

from .models import User, Category, Artwork, Page, Page_type, Image

def sort_after_navigation_order():
    categories = list(Category.objects.all().values())
    pages = list(Page.objects.all().values())
    all = categories + pages
    new_all = sorted(all, key=lambda d: (d["navigation_order"] or len(all) + 2))
    for index, item in enumerate(new_all):
        logger.info(item)
        if item["navigation_order"] and "banner" in item:
            page = Page.objects.get(id=item["id"])
            page.navigation_order = index + 1
            page.save()
        elif item["navigation_order"]:
            category = Category.objects.get(id=item["id"])
            category.navigation_order = index + 1
            category.save()


def sort_after_priority():
    categories = Category.objects.all().values()
    sorted_catgeories = sorted(categories, key=lambda d: (d["priority"] or len(categories) + 2))
    for index, item in enumerate(sorted_catgeories):
        if item["priority"]:
            category = Category.objects.get(id=item["id"])
            category.priority = index + 1
            category.save()


def artist_as_json(request):
    artist = User.models.find(User=request.user)
    return JsonResponse({ "artist": artist })


def to_response_list(query_set):
    return { "success": list(query_set.values()) }


def home(request):
    categories = list(Category.objects.all().order_by("priority").values())
    return JsonResponse({ "success": categories })


# @csrf_exempt
# @login_required
def nav(request):
    if request.method == "PUT" and request.user.is_authenticated:
        req = json.loads(request.body)
        all_nav_items = req["all"]

        for item in all_nav_items:
            current = None
            if "banner" in item:
                current = Page.objects.get(id=item["id"])
            else:
                current = Category.objects.get(id=item["id"])
            
            current.navigation_order = None
            current.save()

        for item in all_nav_items:
            current = None
            if "banner" in item:
                current = Page.objects.get(id=item["id"])
            else:
                current = Category.objects.get(id=item["id"])
            
            current.navigation_order = item["navigationOrder"]
            current.save()

        return JsonResponse({ "success": "Navigation has been updated"})

    logger.info(request.COOKIES)
    page = Page.objects.filter(navigation_order__gt=0).values()
    category = Category.objects.filter(navigation_order__gt=0).values()
    nav = list(page) + list(category)
    sorted_nav = sorted(nav, key=lambda nav_item : nav_item['navigation_order'])
    return JsonResponse({ "success": sorted_nav })


def about(request):
    return artist_as_json(request)


# @csrf_exempt
@login_required
def images(request):
    if request.method == "POST":
        req = json.loads(request.body)
        new_image = Image(
            url = req["url"],
            public_id = req["public_id"]
        )
        new_image.save()
        return JsonResponse({ "success": "Image has been added"})


def contact(request):
    return artist_as_json(request)
    

def all(request):
    categories = Category.objects.all()
    new_categories = []
    for category in categories:
        new_category = {
            "id": category.id,
            "name": category.category,
            "navigation_order": category.navigation_order,
            "priority": category.priority,
            "text": category.text,
        }
        category_pages = list(category.page.all())
        new_category_pages = []

        for page in category_pages:
            new_category_pages.append(page.page)
        
        new_category["page"] = new_category_pages
        new_categories.append(new_category)
    
    art = Artwork.objects.all()
    new_art = []
    for artwork in art:
        new_artwork = {
            "id": artwork.id,
            "name": artwork.title,
            "image": artwork.image,
            "year": artwork.year,
        }
        artwork_category = list(artwork.category.all())
        new_artwork_category = []

        for category in artwork_category:
            new_artwork_category.append(category.category)
        
        new_artwork["category"] = new_artwork_category
        new_art.append(new_artwork)

    pages = list(Page.objects.all().values())
    for page in pages:
        page["page_type"] = page.pop("page_type_id")
        page["name"] = page.pop("page")
    
    page_types = list(Page_type.objects.all().values())

    images = list(Image.objects.all().values())

    all_dict = { 
        "categories": new_categories, 
        "art": new_art, 
        "pages": pages, 
        "page_types": page_types,
        "images": images
    }

    return JsonResponse({ "success": all_dict })




# @csrf_exempt
@login_required
def pages(request):
    if request.method == "DELETE":
        req = json.loads(request.body)
        Page.objects.get(id=req["id"]).delete()
        sort_after_navigation_order()
        return JsonResponse({ "success": "Page has been deleted"})

    else:
        pages = Page.objects.all()
        return JsonResponse(to_response_list(pages))
    

# @csrf_exempt
@login_required
def artworks(request):
    if request.method == "DELETE":
        req = json.loads(request.body)
        Artwork.objects.get(id=req["id"]).delete()
        return JsonResponse({ "success": "Artwork has been deleted"})

    else:
        art = Artwork.objects.all()
        return JsonResponse(to_response_list(art))


# @csrf_exempt
@login_required
def artwork(request, art_id):

    user = User.objects.get(id=1)

    if request.method == "POST" or request.method == "PUT":
        req = json.loads(request.body)
        title = req["name"].strip()
        image = req["image"].strip()
        year = req["year"].strip()
        categories = req["category"]

        if len(title) < 3:
            return JsonResponse({ "error": "Title must have at least two characters"}, status=400)
        
        if len(year) != 4:
            return JsonResponse({ "error": "Year must consist of four characters"}, status=400)
        
        if not year.isnumeric():
            return JsonResponse({ "error": "Year must consist of only numbers"}, status=400)
        
        new_artwork = None

        if request.method == "POST":
            new_artwork = Artwork(
                title = title,
                image = image,
                year = int(year),
                artist = user
            )
            new_artwork.save()

            
        if request.method == "PUT":
            new_artwork = Artwork.objects.get(id=art_id)
            new_artwork.category.clear()
            new_artwork.title = title
            new_artwork.image = image
            new_artwork.year = int(year)

        if len(categories) > 0:
            for category in categories:
                new_artwork.category.add(Category.objects.get(category=category))

        new_artwork.save()

        action = "saved"
        if request.method == "PUT":
            action = "Updated"

        return JsonResponse({ "success": f"Artwork has been {action}"})  
    
    if request.method == "DELETE":
        artwork = Artwork.objects.get(id=art_id)
        artwork.delete()
        return JsonResponse({ "success": "Artwork has been deleted"})
    

# @csrf_exempt
@login_required
def page(request, page_id):

    if request.method == "POST" or request.method == "PUT":
        req = json.loads(request.body)
        page = req["name"].strip()
        page_type = req["pageType"]
        text = req["text"].strip()
        banner = req["banner"]
        page_img = req["pageImg"]
        category_priority = req["categoryPriority"]

        if len(page) < 3:
            return JsonResponse({ "error": "Page name must have at least two characters"}, status=400)
        
        new_page = None

        page_type_set = Page_type.objects.get(page_type=page_type)

        if request.method == "POST":
            new_page = Page(
                page = page,
                page_type = page_type_set,
                text = text,
                banner = banner,
                page_img = page_img
            )
            
        if request.method == "PUT":
            new_page = Page.objects.get(id=page_id)
            new_page.page = page
            new_page.page_type = page_type_set
            new_page.text = text
            new_page.banner = banner
            new_page.page_img = page_img

        new_page.save()

        if page_type == "Home" and category_priority["isChanged"] == True:
            for prio_category in category_priority["categories"]:
                category = Category.objects.get(id=prio_category["id"])
                category.priority = prio_category["priority"]
                category.save()

        action = "saved"
        if request.method == "PUT":
            action = "Updated"

        return JsonResponse({ "success": f"Page has been {action}"})  
    
    if request.method == "DELETE":
        page = Page.objects.get(id=page_id)
        page.delete()
        sort_after_navigation_order()
        return JsonResponse({ "success": "Page has been deleted"})
    

# @csrf_exempt
@login_required
def categories(request):
    if request.method == "DELETE":
        req = json.loads(request.body)
        Category.objects.get(id=req["id"]).delete()
        sort_after_navigation_order()
        sort_after_priority()
        return JsonResponse({ "success": "Category has been deleted"})

    else:
        categories = Category.objects.all()
        return JsonResponse(to_response_list(categories))


# @csrf_exempt
@login_required
def category(request, category_id):

    if request.method == "POST":
        req_category = json.loads(request.body)["category"]
        req_text = json.loads(request.body)["text"]

        if len(req_category) < 3:
            return JsonResponse({ "error": "Category must have at least two characters"}, status=400)
        
        new_category = Category(
            category = req_category,
            text = req_text
        )
        new_category.save()
        return JsonResponse({ "success": "Category has been created"})  

    category = Category.objects.get(id=category_id)

    if request.method == "PUT":
        req_category = json.loads(request.body)["category"]
        req_text = json.loads(request.body)["text"]

        if len(req_category) < 3:
            return JsonResponse({ "error": "Category must have at least two characters"}, status=400)

        category.category = req_category
        category.text = req_text
        category.save()
        return JsonResponse({ "success": "Category has been updated"})
    
    if request.method == "DELETE":
        category.delete()
        sort_after_navigation_order()
        sort_after_priority()

        return JsonResponse({ "success": "Category has been deleted"})

    else:
        category = { 
            "id": getattr(category, "id"), 
            "category": getattr(category, "category"), 
            "priority": getattr(category, "priority"),
            "text": getattr(category, "text"),
        }
        return JsonResponse({ "success": category})


def art(request, category_id):
    category = Category.objects.get(id=category_id)
    art = Artwork.objects.filter(category=category)
    return JsonResponse(to_response_list(art))


# @login_required
def check_authentication(request):
    is_authenticated = request.user.is_authenticated
    return JsonResponse({ "success": { "isAuthenticated": is_authenticated, "cookies": request.COOKIES }})


@csrf_exempt
# @login_required
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
            auth_login(request, user)
            response = JsonResponse({ "success": { "name": getattr(user, "first_name"), "email": getattr(user, "email") } })
            # response.set_cookie("Test", "Please work", httponly=False, domain="api.gunilla-arno-toll.se")
            return response
        else:
            return JsonResponse({ "error": error}, status=401)