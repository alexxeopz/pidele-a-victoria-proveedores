from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mi-negocio/', include('catalogo.urls_proveedor')),

    path('cuenta/ingresar/', auth_views.LoginView.as_view(
        template_name='cuentas/login.html'), name='login'),
    path('cuenta/salir/', auth_views.LogoutView.as_view(), name='logout'),

    path('cuenta/recuperar/', auth_views.PasswordResetView.as_view(
        template_name='cuentas/password_reset.html',
        email_template_name='cuentas/password_reset_email.txt',
        subject_template_name='cuentas/password_reset_subject.txt',
    ), name='password_reset'),
    path('cuenta/recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='cuentas/password_reset_done.html'), name='password_reset_done'),
    path('cuenta/recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='cuentas/password_reset_confirm.html'), name='password_reset_confirm'),
    path('cuenta/recuperar/listo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='cuentas/password_reset_complete.html'), name='password_reset_complete'),

    path('', include('catalogo.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
