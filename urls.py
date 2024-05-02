from django.urls import path
from. import views

urlpatterns = [
    path("containers/", views.container_list, name="container_list"),
]
