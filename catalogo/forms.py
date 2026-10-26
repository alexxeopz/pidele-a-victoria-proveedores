import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Categoria, Producto, TipoMadera, Vendedor

CLIENTE = 'CLIENTE'
PROVEEDOR = 'PROVEEDOR'


def normalizar_whatsapp(valor):
    """Deja solo dígitos: wa.me no acepta signos ni espacios en el número."""
    digitos = re.sub(r'\D', '', valor or '')
    if len(digitos) < 11:
        raise forms.ValidationError(
            'Escribe el número con código de país y sin signos. Ej: 56912345678'
        )
    return digitos


class RegistroForm(UserCreationForm):
    """Registro con dos caminos: cliente o proveedor.

    Los campos del negocio solo se exigen —y solo se muestran— cuando la
    persona elige la opción de proveedor.
    """

    CAMPOS_PROVEEDOR = ['nombre_negocio', 'sector', 'whatsapp']

    tipo_cuenta = forms.ChoiceField(
        label='¿Cómo vas a usar la app?',
        choices=[
            (CLIENTE, 'Soy cliente — quiero pedir leña, carbón o pellet'),
            (PROVEEDOR, 'Soy proveedor — quiero publicar mis productos'),
        ],
        initial=CLIENTE,
        widget=forms.RadioSelect,
    )
    email = forms.EmailField(
        label='Correo electrónico',
        help_text='Lo usamos solo para recuperar tu contraseña.',
    )
    nombre_negocio = forms.CharField(
        label='Nombre de tu negocio', max_length=120, required=False,
        help_text='Es el nombre que verán los clientes en tu perfil.',
    )
    sector = forms.CharField(
        label='Sector desde donde despachas', max_length=120, required=False,
        help_text='Ej: Victoria centro, camino a Traiguén.',
    )
    whatsapp = forms.CharField(
        label='WhatsApp', max_length=15, required=False,
        help_text='Con código de país, solo números. Ej: 56912345678',
    )

    field_order = [
        'tipo_cuenta', 'nombre_negocio', 'sector', 'whatsapp',
        'username', 'email', 'password1', 'password2',
    ]

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {'username': 'Nombre de usuario'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('usable_password', None)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo.')
        return email

    def clean_whatsapp(self):
        valor = self.cleaned_data.get('whatsapp')
        if not valor:
            return valor
        return normalizar_whatsapp(valor)

    def clean(self):
        datos = super().clean()
        if datos.get('tipo_cuenta') == PROVEEDOR:
            for campo, mensaje in [
                ('nombre_negocio', 'Indica el nombre de tu negocio.'),
                ('sector', 'Indica desde qué sector despachas.'),
                ('whatsapp', 'Necesitamos tu WhatsApp para que los clientes te contacten.'),
            ]:
                if not datos.get(campo):
                    self.add_error(campo, mensaje)
        return datos

    def save(self, commit=True):
        usuario = super().save(commit)
        if self.cleaned_data.get('tipo_cuenta') == PROVEEDOR:
            Vendedor.objects.create(
                usuario=usuario,
                nombre=self.cleaned_data['nombre_negocio'],
                sector=self.cleaned_data['sector'],
                whatsapp=self.cleaned_data['whatsapp'],
            )
        return usuario


class PerfilProveedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = [
            'nombre', 'sector', 'whatsapp', 'descripcion',
            'despacha_fuera', 'despacho_fuera_desde',
        ]
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}

    def clean_whatsapp(self):
        return normalizar_whatsapp(self.cleaned_data.get('whatsapp'))

    def clean(self):
        datos = super().clean()
        if not datos.get('despacha_fuera'):
            datos['despacho_fuera_desde'] = None
        return datos


class ProductoProveedorForm(forms.ModelForm):
    """El proveedor gestiona su propio catálogo: no elige vendedor, es él mismo."""

    class Meta:
        model = Producto
        fields = [
            'categoria', 'tipo_madera', 'precio', 'unidad',
            'descripcion', 'imagen', 'disponible',
        ]
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_madera'].choices = [
            ('', 'No aplica (carbón o pellet)'), *TipoMadera.choices
        ]

    def clean(self):
        datos = super().clean()
        if datos.get('categoria') == Categoria.LENA:
            if not datos.get('tipo_madera'):
                self.add_error('tipo_madera', 'La leña necesita un tipo de madera.')
        else:
            datos['tipo_madera'] = ''
        return datos
