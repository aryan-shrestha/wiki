from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/",views.entry_page_view, name="entry_page_view"),
    path("create/new_page/", views.create_entry, name="create_new_page"),
    path("update/<str:title>/", views.update_entry, name="update_page"),
    path("random/page/", views.random_page, name="random_page"),
]
