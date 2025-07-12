from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path("categories/", views.category_select, name="category_select"),
    path("categories/baby-food/", views.baby_food_list, name="baby_food_list"),
    path('search/', views.search, name='search'),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("shelf_stable/", views.shelf_stable, name="shelf_stable"),
    path('categories/shelf-stable/dry-goods/', views.dry_goods, name='dry_goods'),

]
