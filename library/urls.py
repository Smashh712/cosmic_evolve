from django.contrib import admin
from django.urls import path,include
from library import views

app_name = 'library'

urlpatterns = [
    path('search/', views.search, name='search'),
    path('detail/', views.detail, name='detail'),
    path('book_add/', views.book_add, name='book_add'),
    path('show_book_list/', views.show_book_list, name='show_book_list'),
    path('index/', views.index, name='index'),
    path('library/<int:question_id>/', views.detail_index, name='detail_index'),
    path('answer/create/<int:question_id>/', views.answer_create, name="answer_create"),
]