from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)


#
#admin.site.register(Category, DraggableMPTTAdmin)
# admin.site.register(Product, DraggableMPTTAdmin)
