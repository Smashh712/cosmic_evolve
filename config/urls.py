from django.contrib import admin
from django.urls import path, include
from library import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("library/", include("library.urls")),
    path("accounts/", include("accounts.urls")),
    path('', views.index, name='index_main'),

]
