from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView

from django.views.decorators.cache import cache_page

from .models import Profile
from .forms import UserForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _, ngettext

from random import random
# Create your views here.

class HelloView(View): # локализация данных
    welcome_message = _("welcome hello world")

    def get(self, request: HttpRequest):
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_message}</h1>"
            f"\n<h2>{products_line}</h2>"
        )




def login_view(request: HttpRequest):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')
    return render(request, "myauth/login.html", {"error": "Invalid login credentials"})

# class AboutMeView(TemplateView):
#     template_name = 'myauth/about-me.html'

class AboutMeView(DetailView):
    template_name = 'myauth/about-me.html'
    queryset = User.objects.all()
    context_object_name = 'user'

class UserListView(ListView):
    template_name = 'myauth/users-list.html'
    # model = Product
    queryset = User.objects.all()
    context_object_name = 'users'

class UserUpdateView(UpdateView):
    model = User
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    form_class = UserForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            'myauth:about-me',
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
            responce = super().form_valid(form)
            bio = form.cleaned_data["bio"]
            image = form.files.get("images")
            try:
                tom = Profile.objects.get(user_id=self.object.pk)
                tom.user = self.object
                tom.bio = bio
                tom.image = image
                tom.save()
            except ObjectDoesNotExist:
                Profile.objects.create(
                    user=self.object,
                    bio=bio,
                    image=image
                )
            return responce


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        responce = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return responce
def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse("myauth:login"))

# class MyLogoutView(LogoutView):
#     next_page = reverse_lazy("myauth:login")

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest):
    responce = HttpResponse("Cookie set")
    responce.set_cookie("fizz", "buzz", max_age=3600)
    return responce

@cache_page(20 * 1)                                        # кэширование на 20 секунд
def get_cookie_view(request: HttpRequest):
    value =request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")

@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest):
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")

@login_required
def get_session_view(request: HttpRequest):
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")



class FooBarView(View):
    def get(self, request: HttpRequest):
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})