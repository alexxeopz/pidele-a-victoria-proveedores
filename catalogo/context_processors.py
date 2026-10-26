def perfil(request):
    """Expone a las plantillas si el usuario que navega es proveedor."""
    return {'es_proveedor': hasattr(request.user, 'vendedor')}
