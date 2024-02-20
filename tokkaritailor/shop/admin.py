from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'id']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)    
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)