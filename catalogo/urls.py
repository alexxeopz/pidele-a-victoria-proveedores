from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('proveedor/<int:pk>/', views.detalle_vendedor, name='detalle_vendedor'),
    path('cuenta/registro/', views.registro, name='registro'),
]
