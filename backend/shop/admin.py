from django.contrib import admin
from .models import Category, Product, ProductImage
from django_json_widget.widgets import JSONEditorWidget  
from django.db import models
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'id']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'id']
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},  # Редактор JSON для fields
}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]  

    def get_changeform_initial_data(self, request):

        """
        Метод для обработки изменения формы
        """

        initial = super().get_changeform_initial_data(request)
        category_id = request.GET.get('category')

        if category_id:
            try:
                category = Category.objects.get(pk=category_id)
                initial['characteristics'] = category.characteristics_template
            except Category.DoesNotExist:
                pass

        return initial


    def add_view(self, request, form_url='', extra_context=None):
        
        """
        Динамическое добавление query параметра в URL для новых товаров в категории
        """

        category_id = request.GET.get('category')
        if category_id:
            form_url += '?category=' + category_id
        return super().add_view(request, form_url, extra_context)


admin.site.register(Category, CategoryAdmin)    
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)