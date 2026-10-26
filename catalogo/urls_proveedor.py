from django.urls import path

from . import views_proveedor

app_name = 'proveedor'

urlpatterns = [
    path('', views_proveedor.perfil, name='perfil'),
    path('productos/nuevo/', views_proveedor.producto_form, name='producto_crear'),
    path('productos/<int:pk>/editar/', views_proveedor.producto_form, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views_proveedor.producto_eliminar,
         name='producto_eliminar'),
]
