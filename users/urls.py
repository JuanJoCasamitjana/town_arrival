from django.urls import path
from .views import user_login, register, update_profile

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('update-profile/', update_profile, name='update_profile'),
    # Otras rutas de tus vistas
]
