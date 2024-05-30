from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from . import views

app_name = "shopapp"

routers = DefaultRouter()
routers.register("product", views.ProductViewSet)

urlpatterns = [
       # path('', cache_page(20 * 1)(views.ShopIndexView.as_view()), name="index"),          # кеширование отдельного представления на определенное время
       path('', views.ShopIndexView.as_view(), name="index"),
       path('api/', include(routers.urls)),
       path('groups/', views.GroupListView.as_view(), name="group_list"),
       path('products/', views.ProductListView.as_view(), name="products_list"),
       path('products/latest/feed/', views.LatestProductsFeed(), name="products-feed"),
       path('products/export', views.ProductsDataExportView.as_view(), name="products-export"),
       path('products/create', views.ProductCreateView.as_view(), name="product_create"),
       # path('products/create', views.create_product, name="product_create"),
       path('products/<int:pk>', views.ProductDetailView.as_view(), name="product_details"),
       path('products/<int:pk>/update', views.ProductUpdateView.as_view(), name="product_update"),
       path('products/<int:pk>/confirm-delete', views.ProductDeleteView.as_view(), name="product_delete"),
       path('orders/', views.OrdersListView.as_view(), name="orders_list"),
       path('orders/<int:pk>', views.OrdersDetailView.as_view(), name="order_details"),
       path('orders/create', views.create_order, name="order_create"),
]

# urlpatterns = [
#        path('', views.shop_index, name="index"),
#        path('groups/', views.group_list, name="group_list"),
#        path('products/', views.products_list, name="products_list"),
#        path('products/create', views.create_product, name="product_create"),
#        path('orders/', views.orders_list, name="orders_list"),
#        path('orders/create', views.create_order, name="order_create"),
# ]