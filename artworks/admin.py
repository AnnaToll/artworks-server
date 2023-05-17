from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Artwork, Page, Page_type, Banner

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Artwork)
admin.site.register(Page)
admin.site.register(Page_type)
admin.site.register(Banner)