from django.urls import path
from .views import user_login, register, update_profile, user_logout

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('update-profile/', update_profile, name='update_profile'),
    # Otras rutas de tus vistas
]
