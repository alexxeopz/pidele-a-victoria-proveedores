from django.contrib import admin

from .models import Producto, Vendedor


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sector', 'whatsapp', 'usuario', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'sector')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_publico', 'vendedor', 'categoria', 'precio', 'unidad', 'disponible')
    list_filter = ('categoria', 'tipo_madera', 'unidad', 'disponible', 'vendedor')
    search_fields = ('vendedor__nombre', 'descripcion')
