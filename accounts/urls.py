from django.urls import path
from .views import admin_login, admin_register, admin_dashboard

urlpatterns = [
    path("admin_login/",admin_login, name="admin_login"),
    path("register/", admin_register, name="admin_register"),
    path("admin_dashboard/",admin_dashboard, name="admin_dashboard"),
]