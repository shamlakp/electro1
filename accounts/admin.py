from django.contrib import admin
from products.models import Category 
# Register your models here.

 
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
