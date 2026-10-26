from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistroForm
from .models import Vendedor


def inicio(request):
    contexto = {
        'proveedores': Vendedor.objects.filter(activo=True).prefetch_related('productos'),
    }
    return render(request, 'catalogo/inicio.html', contexto)


def detalle_vendedor(request, pk):
    vendedor = get_object_or_404(Vendedor, pk=pk, activo=True)
    return render(request, 'catalogo/detalle_vendedor.html', {
        'vendedor': vendedor,
        'productos': vendedor.productos.publicados(),
    })


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            if hasattr(usuario, 'vendedor'):
                messages.success(
                    request, f'Listo {usuario.username}, ya puedes cargar tus productos.'
                )
                return redirect('proveedor:perfil')
            messages.success(request, f'Bienvenido {usuario.username}.')
            return redirect('catalogo:inicio')
    else:
        form = RegistroForm()
    return render(request, 'cuentas/registro.html', {
        'form': form, 'campos_proveedor': RegistroForm.CAMPOS_PROVEEDOR,
    })
