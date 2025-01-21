from django.contrib import admin
from .models import CarMake, CarModel

# Inline class for CarModel within CarMake admin
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Allows adding one CarModel inline within CarMake

# Admin class for CarMake
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']
    search_fields = ['name']

# Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'car_type', 'year']
    list_filter = ['car_type', 'year']
    search_fields = ['name']

# Register models
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)


