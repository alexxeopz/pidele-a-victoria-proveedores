from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PerfilProveedorForm, ProductoProveedorForm
from .models import Producto


def proveedor_requerido(vista):
    """Solo entra quien tiene un perfil de proveedor asociado a su cuenta."""

    @wraps(vista)
    @login_required
    def envoltorio(request, *args, **kwargs):
        vendedor = getattr(request.user, 'vendedor', None)
        if vendedor is None:
            messages.error(request, 'Esta sección es solo para proveedores registrados.')
            return redirect('catalogo:inicio')
        return vista(request, vendedor, *args, **kwargs)

    return envoltorio


@proveedor_requerido
def perfil(request, vendedor):
    form = PerfilProveedorForm(request.POST or None, instance=vendedor)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Actualizaste los datos de tu negocio.')
        return redirect('proveedor:perfil')
    return render(request, 'proveedor/perfil.html', {
        'form': form, 'vendedor': vendedor, 'productos': vendedor.productos.all(),
    })


@proveedor_requerido
def producto_form(request, vendedor, pk=None):
    producto = get_object_or_404(Producto, pk=pk, vendedor=vendedor) if pk else None
    form = ProductoProveedorForm(request.POST or None, request.FILES or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        guardado = form.save(commit=False)
        guardado.vendedor = vendedor
        guardado.save()
        messages.success(request, f'Guardaste "{guardado.nombre_publico}".')
        return redirect('proveedor:perfil')
    return render(request, 'proveedor/producto_form.html', {
        'form': form,
        'titulo': 'Editar producto' if producto else 'Agregar producto',
        'producto': producto,
    })


@proveedor_requerido
def producto_eliminar(request, vendedor, pk):
    producto = get_object_or_404(Producto, pk=pk, vendedor=vendedor)
    if request.method == 'POST':
        nombre = producto.nombre_publico
        producto.delete()
        messages.success(request, f'Eliminaste "{nombre}" de tu catálogo.')
        return redirect('proveedor:perfil')
    return render(request, 'proveedor/producto_eliminar.html', {'producto': producto})
