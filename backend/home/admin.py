from django.contrib import admin
from .models import HomePageImage

@admin.register(HomePageImage)
class HomePageImageAdmin(admin.ModelAdmin):
    list_display = ('description', 'image',)
