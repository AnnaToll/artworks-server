from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"User: {self.username}"
    

class Page_type(models.Model):
    page_type = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f"Page type: {self.page_type}"
    

class Image(models.Model):
    url = models.URLField(max_length=500)
    public_id = models.CharField(max_length=50)

    def __str__(self):
        return f"Public_id: {self.public_id}"    
    

class Page(models.Model):
    page = models.CharField(max_length=30)
    navigation_order = models.PositiveSmallIntegerField(unique=True, blank=True, null=True)
    page_type = models.ForeignKey(Page_type, on_delete=models.SET_NULL, null=True, to_field="page_type")
    text = models.TextField(blank=True, default="")
    banner = models.URLField(max_length=500, blank=True, null=True)
    page_img = models.URLField(max_length=500, blank=True, null=True)


    def __str__(self):
        return f"Page: {self.page}, {self.page_type}"    
    

class Category(models.Model):
    category = models.CharField(max_length=30)
    page = models.ManyToManyField(Page, blank=True)
    navigation_order = models.PositiveSmallIntegerField(unique=True, blank=True, null=True)
    priority = models.PositiveSmallIntegerField(blank=True, null=True)
    text = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Category: {self.category}"


class Artwork(models.Model):
    title = models.CharField(blank=True, max_length=200)
    image = models.URLField(max_length=500, blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Artwork: {self.title}, year: {self.year}"
    
