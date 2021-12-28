from django.contrib import admin
from django.urls import path,include
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', views.search, name='search'),
    path('detail/', views.detail, name='detail'),
    path('book_add/', views.book_add, name='book_add'),
    path('show_book_list/', views.show_book_list, name='show_book_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
