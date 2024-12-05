from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Nombre d'images additionnelles par défaut affichées

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'landlord', 'price_per_night', 'created_at')
    search_fields = ('title', 'landlord__username')
    list_filter = ('landlord', 'created_at')
    inlines = [PropertyImageInline]  # Affiche les images additionnelles directement dans la page de la propriété

# Enregistrer le modèle PropertyImage (si vous souhaitez gérer ces images indépendamment)
@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image', 'created_at', 'property__title',)
    search_fields = ('property__title',)
    list_filter = ('property',)
