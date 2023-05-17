from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to="other", blank=True)

    def __str__(self):
        return f"User: {self.username}"
    

class Page_type(models.Model):
    page_type = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"Page type: {self.page_type}"
    

class Banner(models.Model):
    image = models.ImageField(upload_to="img", unique=True)

    def __str__(self):
        return f"Banner: {self.image}"
    

class Page(models.Model):
    page = models.CharField(max_length=30)
    navigation_order = models.PositiveSmallIntegerField(unique=True, blank=True, null=True)
    page_type = models.ForeignKey(Page_type, on_delete=models.SET_NULL, null=True, to_field="page_type")
    text = models.TextField(blank=True, default="")
    banner = models.ForeignKey(Banner, on_delete=models.SET_NULL, blank=True, null=True, to_field="image")
    page_img = models.ImageField(upload_to="img", blank=True)


    def __str__(self):
        return f"Page: {self.page}, {self.page_type}"    
    

class Category(models.Model):
    category = models.CharField(max_length=30)
    page = models.ManyToManyField(Page, blank=True)
    navigation_order = models.PositiveSmallIntegerField(unique=True, blank=True, null=True)
    priority = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Category: {self.category}"


class Artwork(models.Model):
    title = models.CharField(blank=True, max_length=200)
    image = models.ImageField(upload_to="artworks")
    category = models.ManyToManyField(Category)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Artwork: {self.title}, year: {self.year}, by: {self.artist}"
    
