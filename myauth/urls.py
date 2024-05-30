from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

app_name = "myauth"

urlpatterns = [
       # path('login/', views.login_view, name="login"),
       path('login/',
            LoginView.as_view(template_name="myauth/login.html", redirect_authenticated_user=True,),
            name="login"),
       path('logout/', views.logout_view, name="logout"),
       path('users/', views.UserListView.as_view(), name="users_list"),
       path('users/<int:pk>/about-me', views.AboutMeView.as_view(), name="about-me"),
       path('users/<int:pk>/about-me/update',
            views.UserUpdateView.as_view(template_name="myauth/user_update_form.html"),
            name="user_update"),
       path('register/', views.RegisterView.as_view(), name="register"),
       # path('logout/', views.MyLogoutView.as_view(), name="logout"), # не работает в 5.0
       path("cookie/get/", views.get_cookie_view, name="cookie-get"),
       path("cookie/set/", views.set_cookie_view, name="cookie-set"),
       path("session/set/", views.set_session_view, name="session-get"),
       path("session/get/", views.get_session_view, name="session-set"),
       path("foo-bar/", views.FooBarView.as_view(), name="foo-bar"),
       path("hello/", views.HelloView.as_view(), name="hello"),

]