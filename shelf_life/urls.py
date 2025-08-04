from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('search/', views.search, name='search'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('about/', views.about, name='about'),
    path('donate/', views.donate, name='donate'),
    path('sources/', views.sources, name='sources'),
    path('resources/', views.resources, name='resources'),
    path('contact/', views.contact, name='contact'),


    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    # path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path('coming-soon/', views.coming_soon, name='coming_soon'),

    path("categories/", views.category_select, name="category_select"),
    path("categories/baby-food/", views.baby_food_list, name="baby_food_list"),
    path("categories/shelf_stable/", views.shelf_stable, name="shelf_stable"),
    
    # dry goods
    path("categories/shelf_stable/dry_goods/", views.dry_goods_subcategories, name="dry_goods_subcategories"),
    path('categories/shelf-stable/dry-goods/<slug:category_slug>/', views.dry_goods_category_detail, name='dry_goods_category_detail'),

    # shelf stable beverages
    path('categories/shelf-stable/beverages/', views.ssb_categories, name='ssb_categories'),
    path('categories/shelf-stable/dry-goods/beverages/<slug:category_slug>/', views.ssb_category_detail, name='ssb_category_detail'),
    
    # other shelf stable categories
    path('categories/shelf-stable/<str:subcategory>/', views.shelf_stable_detail, name='shelf_stable_detail'),
    # refrigerated categories
    path('categories/refrigerated/', views.refrigerated_categories, name='refrigerated_categories'),
    path('categories/refrigerated/<str:category>/', views.refrigerated_intermediate, name='refrigerated_intermediate'),
    path('categories/refrigerated/<str:category>/<str:subcategory>/', views.refrigerated_category_detail, name='refrigerated_category_detail'),

    # frozen categories
    path('categories/frozen/meat-poultry-seafood/', views.frozen_meat_categories, name='frozen_meat_categories'),
    path('categories/frozen/meat-poultry-seafood/<str:meat_subcategory>/', views.frozen_meat_category_detail, name='frozen_meat_category_detail'),
    path('categories/frozen/', views.frozen_categories, name='frozen_categories'),
    path('categories/frozen/<str:subcategory>/', views.frozen_category_detail, name='frozen_category_detail'),

]