from django.urls import path
from . import views

app_name = "myapiapp"

urlpatterns = [
       path('hello/', views.hello_world_view, name="hello"),
       path('groups/', views.GroupsListView.as_view(), name="groups"),
]