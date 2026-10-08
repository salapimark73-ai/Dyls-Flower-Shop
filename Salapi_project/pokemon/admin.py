from django.contrib import admin
from .models import Flower

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('flower_name', 'flower_type', 'price', 'quantity', 'color', 'date_added')
    list_filter = ('flower_type', 'color')
    search_fields = ('flower_name', 'color', 'description')
