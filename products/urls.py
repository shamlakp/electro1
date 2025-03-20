
from django.urls import path
from .views import public_login, public_register, product_list,profile,add_product,product_detail, category_list_view,delete_account,edit_product,delete_product
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("public_login/", public_login, name="public_login"),
    path("register/", public_register, name="public_register"),
    path("product_list/", product_list, name="product_list"),
    path("profile/", profile, name="profile"),
    path("add_product/", add_product, name='add_product'),
    path("product/<int:product_id>/", product_detail, name='product_detail'),
    path("categories/", category_list_view, name='category_list'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("delete_account/", delete_account, name='delete_account'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
     path('delete_product/<int:product_id>/', delete_product, name='delete_product')
]
