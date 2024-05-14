from django.contrib import admin

# Register your models here.

from store.models import Category,Size,Product,Brand

admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Brand)
