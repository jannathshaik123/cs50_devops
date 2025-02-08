from django.urls import path
from . import views

app_name = "tasks"
urlpatterns = [
    path("",views.index, name="index"),
    path("add",views.add_tasks, name="add_tasks")
]
