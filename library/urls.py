from django.contrib import admin
from django.urls import path, include
from library import views


app_name = "library"

urlpatterns = [
    path('bookAdd/', views.bookAdd, name="bookAdd"),
    path('printBooks/', views.printBooks, name="printBooks"),
    path('index/', views.index, name='index'),
    path('returnBook/', views.returnBook, name='returnBook'),
    path('search/', views.search, name='search'),
    path('detail/', views.detail, name='detail'),
    path('rentBook/', views.rentBook, name='rentBook'),
    path('home/', views.home, name="home"),
    path('rentalReturnBook/', views.rentalReturnBook, name='rentalReturnBook'),
    path('myBookList/', views.myBookList, name='myBookList'),
    
    
]