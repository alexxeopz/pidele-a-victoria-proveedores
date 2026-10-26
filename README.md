# PideLeña Victoria — módulo de cuentas y catálogo de proveedores

Módulo de una plataforma web que conecta a vecinos de Victoria (Región de La Araucanía, Chile)
con proveedores de leña, carbón y pellet.

Este repositorio contiene **solo dos partes** del sistema:

1. **Cuentas**: registro diferenciado entre cliente y proveedor, inicio de sesión, cierre de
   sesión y recuperación de contraseña por correo.
2. **Catálogo del proveedor**: cada proveedor administra los datos de su negocio y publica,
   edita y elimina sus propios productos, con fotografía incluida.

## Qué hace

- El registro pregunta primero el tipo de cuenta. Los campos del negocio (nombre, sector y
  WhatsApp) solo aparecen al elegir la opción de proveedor; el formulario se adapta con
  JavaScript y la validación se repite en el servidor, de modo que funciona igual sin él.
- El número de WhatsApp se normaliza a solo dígitos al guardarlo, porque los enlaces de
  contacto de WhatsApp no aceptan espacios ni signos.
- La sección «Mi negocio» reúne en una pantalla los datos del proveedor y su catálogo.
- Los precios se publican **puestos en Victoria**, con el despacho urbano incluido, para que
  los clientes puedan compararlos entre proveedores. Cada proveedor declara aparte si despacha
  a sectores rurales y desde qué monto.
- El acceso a la sección del proveedor se controla con un decorador que verifica en el servidor
  que la cuenta tenga un perfil de proveedor asociado.

## Tecnologías

| Herramienta | Versión | Uso |
|---|---|---|
| Python | 3.13 | Lenguaje del sistema |
| Django | 6.1 | Framework web: modelos, vistas, formularios y autenticación |
| SQLite | 3 | Base de datos en desarrollo |
| Pillow | 12 | Procesamiento de las imágenes de productos |

## Cómo ejecutarlo

```bash
python -m venv venv
venv\Scripts\activate          # en Linux o macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Luego abre `http://localhost:8000`.

Para entrar al administrador de Django, crea primero una cuenta:

```bash
python manage.py createsuperuser
```

## Rutas principales

| Ruta | Descripción |
|---|---|
| `/` | Listado público de proveedores |
| `/proveedor/<id>/` | Perfil público de un proveedor con su catálogo |
| `/cuenta/registro/` | Registro como cliente o proveedor |
| `/cuenta/ingresar/` | Inicio de sesión |
| `/cuenta/recuperar/` | Recuperación de contraseña |
| `/mi-negocio/` | Datos del negocio y catálogo (solo proveedores) |
| `/admin/` | Administrador de Django |

## Estructura

```
catalogo/
  models.py            Vendedor y Producto
  forms.py             Registro, perfil del proveedor y producto
  views.py             Páginas públicas y registro
  views_proveedor.py   Sección «Mi negocio», protegida por decorador
  templates/           Plantillas de catálogo, cuentas y proveedor
static/css/style.css   Hoja de estilos propia, sin frameworks externos
```

## Notas sobre configuración

El proyecto se ejecuta en modo de desarrollo de forma predeterminada. Para producción, define
estas variables de entorno:

- `DJANGO_SECRET_KEY`: clave secreta propia.
- `DJANGO_DEBUG=0`: desactiva el modo de depuración.
- `DJANGO_ALLOWED_HOSTS`: dominios autorizados, separados por comas.

Además queda pendiente migrar a PostgreSQL y configurar un servidor que entregue los archivos
estáticos y las imágenes subidas, tarea que en desarrollo realiza el propio Django.

Los correos de recuperación de contraseña se imprimen en la consola; para enviarlos de verdad
hay que configurar un servidor SMTP.
