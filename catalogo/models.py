from django.conf import settings
from django.db import models


class Categoria(models.TextChoices):
    LENA = 'LENA', 'Leña'
    CARBON = 'CARBON', 'Carbón'
    PELLET = 'PELLET', 'Pellet'


class TipoMadera(models.TextChoices):
    AROMO = 'AROMO', 'Aromo'
    PINO = 'PINO', 'Pino'
    EUCALIPTO = 'EUCALIPTO', 'Eucalipto'


class Unidad(models.TextChoices):
    METRO_CUBICO = 'M3', 'Metro cúbico'
    MEDIO_METRO = 'MEDIO_M3', 'Medio metro cúbico'
    SACO = 'SACO', 'Saco'
    BOLSA = 'BOLSA', 'Bolsa'
    KILO = 'KILO', 'Kilo'


def formatear_clp(valor):
    return f'{valor:,}'.replace(',', '.')


def describir_producto(categoria, tipo_madera):
    if categoria == Categoria.LENA and tipo_madera:
        return f'leña de {TipoMadera(tipo_madera).label.lower()}'
    return Categoria(categoria).label.lower()


class Vendedor(models.Model):
    """Proveedor de leña, carbón o pellet, asociado a una cuenta de acceso."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='vendedor', verbose_name='cuenta de acceso',
    )
    nombre = models.CharField('nombre', max_length=120)
    sector = models.CharField(
        'sector / localidad', max_length=120,
        help_text='Ej: Victoria centro, Camino a Traiguén, Quechurreguas',
    )
    whatsapp = models.CharField(
        'WhatsApp', max_length=15,
        help_text='Con código de país, solo números. Ej: 56912345678',
    )
    descripcion = models.TextField('descripción', blank=True)
    despacha_fuera = models.BooleanField(
        'despacho fuera de Victoria', default=False,
        help_text='Marca esto si llegas a sectores rurales o localidades cercanas.',
    )
    despacho_fuera_desde = models.PositiveIntegerField(
        'despacho fuera de Victoria, desde (CLP)', null=True, blank=True,
        help_text='Valor referencial. Déjalo vacío si prefieres decir "a convenir".',
    )
    activo = models.BooleanField('activo', default=True)
    creado = models.DateTimeField('creado', auto_now_add=True)

    class Meta:
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.sector})'

    @property
    def descripcion_despacho(self):
        if not self.despacha_fuera:
            return 'Despacha solo dentro de Victoria.'
        if self.despacho_fuera_desde:
            return (
                'Despacha fuera de Victoria desde '
                f'${formatear_clp(self.despacho_fuera_desde)}, según distancia.'
            )
        return 'Despacha fuera de Victoria, con costo a convenir según distancia.'


class ProductoQuerySet(models.QuerySet):
    def publicados(self):
        return self.filter(disponible=True, vendedor__activo=True)


class Producto(models.Model):
    """Producto del catálogo de un proveedor, a precio puesto en Victoria."""

    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE, related_name='productos', verbose_name='proveedor'
    )
    categoria = models.CharField(
        'categoría', max_length=10, choices=Categoria.choices, default=Categoria.LENA
    )
    tipo_madera = models.CharField(
        'tipo de madera', max_length=20, choices=TipoMadera.choices, blank=True,
        help_text='Solo para leña.',
    )
    precio = models.PositiveIntegerField(
        'precio puesto en Victoria (CLP)',
        help_text='Incluye el despacho dentro de Victoria. Es referencial: el monto final '
                  'se acuerda con el cliente.',
    )
    unidad = models.CharField(
        'unidad de venta', max_length=10, choices=Unidad.choices, default=Unidad.METRO_CUBICO
    )
    descripcion = models.TextField('descripción', blank=True)
    imagen = models.ImageField('imagen', upload_to='productos/', blank=True, null=True)
    disponible = models.BooleanField('disponible', default=True)
    creado = models.DateTimeField('creado', auto_now_add=True)

    objects = ProductoQuerySet.as_manager()

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-creado']

    def __str__(self):
        return f'{self.nombre_publico} - {self.vendedor.nombre}'

    @property
    def nombre_publico(self):
        return describir_producto(self.categoria, self.tipo_madera).capitalize()

    @property
    def es_lena(self):
        return self.categoria == Categoria.LENA
