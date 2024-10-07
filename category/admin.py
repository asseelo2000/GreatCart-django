from django.contrib import admin
from .models import Category
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CategoryAdmin(admin.ModelAdmin): 
    prepopulated_fields = {'slug':('category_name',)}   
    list_display = ('category_name', 'slug')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Category, CategoryAdmin)