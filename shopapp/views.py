"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.syndication.views import Feed
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from timeit import default_timer

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, OrderForm, GroupForm
from .models import Product, Order, ProductImage

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .serializers import ProductSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, OpenApiResponse

import logging

from csv import DictWriter
from .common import save_csv_products

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

log = logging.getLogger(__name__)

@extend_schema(description="Product views CRUD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущности товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    search_fields = ["name", "description"]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount"
    ]

    @method_decorator(cache_page(20 * 1))                    # кеширование REST FRAMEWORK через декоратор
    def list(self, *args, **kwargs):
        print("кеширование REST FRAMEWORK")
        return super().list(*args, **kwargs)

    @extend_schema(
        summary="Get one productby ID",
        description="Retrieves **product**, return 404 if not found",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description="Empty responce, product by id not found"),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=['get'], detail=False)                  # выгрузка CSV-файла из БД в rest_framework
    def download_csv(self, request: Request):

        response = HttpResponse(content_type="text/csv")
        filename = "product-export.csv"
        response["Content_Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "description",
            "price",
            "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response

    @action(methods=['post'], detail=False, parser_classes=[MultiPartParser],)
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES["file"].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


# Create your views here.
class ShopIndexView(View):

    # @method_decorator(cache_page(20 * 1))
    def get(self,request: HttpRequest):
      products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
      ]
      context = {
        'time_running': default_timer(),
        'products': products,
        'items': 2,
      }
      log.debug("Products for shop index: %s", products)
      log.info("Rendering shop index")
      print("shop index context", context)
      return render(request, 'shopapp/shop-index.html', context=context)

# def shop_index(request: HttpRequest):
#     products = [
#         ('Laptop', 1999),
#         ('Desktop', 2999),
#         ('Smartphone', 999),
#     ]
#     context = {
#         'time_running': default_timer(),
#         'products': products
#     }
#     return render(request, 'shopapp/shop-index.html', context=context)

class GroupListView(View):
    def get(self, request: HttpRequest):
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/group-list.html', context=context)
    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
           form.save()
        return redirect(request.path)

# def group_list(request: HttpRequest):            # 1 variant
#     context = {
#         'groups': Group.objects.prefetch_related('permissions').all(),
#     }
#     return render(request, 'shopapp/group-list.html', context=context)



# class ProductDetailView(View):                     # 2 variant
#     def get(self, request: HttpRequest, pk: int):
#         # product = Product.objects.get(pk=pk)
#         product = get_object_or_404(Product, pk=pk)
#         context = {
#             'product': product
#         }
#         return render(request, 'shopapp/products-details.html', context=context)

class ProductDetailView(DetailView):                     # 3 variant
    template_name = 'shopapp/products-details.html'
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    # print(queryset.values())
    context_object_name = 'product'



class ProductListView(ListView):            # 3 variant
    template_name = 'shopapp/products-list.html'
    # model = Product
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'

# class ProductListView(TemplateView):      # 2 variant
#     template_name = 'shopapp/products-list.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['product'] = Product.objects.all()
#         return context

# def products_list(request: HttpRequest):  # 1 variant
#     context = {
#        'products': Product.objects.all(),
#     }
#     return render(request, 'shopapp/products-list.html', context=context)

class ProductCreateView(UserPassesTestMixin, CreateView):                # 1 variant
    def test_func(self):
        # return self.request.user.groups.filter(name="secret-group").exists()
        return self.request.user.is_superuser

    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    # form_class = ProductForm
    success_url = reverse_lazy("shopapp:products_list")

class ProductUpdateView(UpdateView):
    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    form_class = ProductForm                 # групповая загрузка картинок  не работает так в 5.0
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        responce = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image
            )
        return responce



class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class ProductsDataExportView(View):
    def get(self, request: HttpRequest):
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {'pk': product.pk,
                 'name': product.name,
                 'price': product.price,
                 'archived': product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        elem = products_data[0]
        name = elem["name"]
        print("name:", name)
        return JsonResponse({"products": products_data})

# def create_product(request: HttpRequest):         # 2 variant
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#            #1 name = form.cleaned_data["name"]
#            #2 Product.objects.create(**form.cleaned_data)
#            form.save()
#            url = reverse("shopapp:products_list")
#            return redirect(url)
#     else:
#         form = ProductForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'shopapp/create-product.html', context=context)

# def orders_list(request: HttpRequest):        # 1 variant
#     context = {
#        'orders':Order.objects.select_related("user").prefetch_related('product').all(),
#     }
#     return render(request, 'shopapp/orders-list.html', context=context)

class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (Order.objects.select_related("user").prefetch_related('product'))

class OrdersDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (Order.objects.select_related("user").prefetch_related('product'))

def create_order(request: HttpRequest):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
           #1 name = form.cleaned_data["name"]
           #2 Product.objects.create(**form.cleaned_data)
           form.save()
           url = reverse("shopapp:order_list")
           return redirect(url)
    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    return render(request, 'shopapp/create-order.html', context=context)


class LatestProductsFeed(Feed):
    title = "Blog products (latest)"
    description = "Updates on changes addition blog products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return (
           Product.objects
           .filter(created_at__isnull=False)
           .order_by("-created_at")[:5]
        )

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]