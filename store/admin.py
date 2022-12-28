from django.contrib import admin
from .models import Truck , Product
# Register your models here.

class TruckAdmin(admin.ModelAdmin):
	list_display = ('name','money_made')
	prepopulated_fields = {"slug": ("name",)}

class ProductAdmin(admin.ModelAdmin):
	list_display = ('name','price','flavour','quantity')
	prepopulated_fields = {"slug": ("name",)}

admin.site.register(Truck,TruckAdmin)
admin.site.register(Product,ProductAdmin)
