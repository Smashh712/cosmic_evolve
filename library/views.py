from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import requests
import xmltodict
from . import models
from django.core.paginator import Paginator


def search(request):
    
    keyword = request.POST.get("user_input")
    isbn = request.POST.get('isbn')
    
    # if(isbn):
    #     url = f"http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey=ttbmlboy101516001&itemIdType=ItemId&itemId={isbn}&output=xml"
    #     test = requests.get(url)
    #     dict_type = xmltodict.parse(test.text)
        
    #     title = dict_type["object"]['item']['title']
    #     author = dict_type['object']['item']['author']
    #     picture = dict_type['object']['item']['cover']
        
    #     list_ = [title, author, picture]
    #     context = {}
        
    #     context["detail"] = list_
        
    #     return render(request, 'detail.html', context)
    
    key = "ttbmlboy101516001"
    list_ = []
    context = {}
    url = f"https://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query={keyword}&QueryType=Title&MaxResults=10&start=1&SearchTarget=Book&output=xml&ItemIdType=ItemId&Version=20070901&Sort=Accuracy&ItemId={isbn}"
    temp = requests.get(url)
    dict_type = xmltodict.parse(temp.text)
    if "item" not in dict_type["object"] :
        list_ = [["책이 없습니다.",None,None]]
    else:
        for i in range(len(dict_type["object"]["item"])):
            if len(dict_type["object"]["item"])  == 18:
                title = dict_type["object"]["item"]["title"]
                author = dict_type["object"]["item"]["author"]
                publisher = dict_type["object"]["item"]["publisher"]
                isbn = dict_type["object"]["item"]["@itemId"]
                list_.append([title, author, publisher, isbn])
                break
            else:
                title = dict_type["object"]["item"][i]["title"]
                author = dict_type["object"]["item"][i]["author"]
                publisher = dict_type["object"]["item"][i]["publisher"]
                isbn = dict_type["object"]["item"][i]["@itemId"]
                list_.append([title,author,publisher,isbn])
            
    context["book"] = list_
    return render(request, 'index.html', context)
        


def detail(request):
    
    isbn = request.POST.get('isbn')
    
    if(isbn):
        url = f" http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey=ttbmlboy101516001&ItemIdType=ItemId&ItemId={isbn}&output=xml"
        
        test = requests.get(url)
        dict_type = xmltodict.parse(test.text)
        
        title = dict_type["object"]['item']['title']
        author = dict_type['object']['item']['author']
        picture = dict_type['object']['item']['cover']
        price = dict_type["object"]["item"]["priceStandard"]
        isbn13 = dict_type['object']['item']['isbn13']
        
        list_ = [title, author, price, picture, isbn13]
        context = {}
        context["detail"] = list_

        return render(request, 'detail.html', context)
    
    else:
        return render(request, 'index.html')
    

# title, author, price, isbn

def book_add(request):
    # 책 추가하기 
    # 책의 isbn으로 추가하기 name이 isbn인 버튼을 클릭시 objects.create 발동
    if request.method == 'POST':
        book_add = request.POST.get('book_add')
        
        url = f" http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey=ttbmlboy101516001&ItemIdType=ItemId&ItemId={book_add}&output=xml"
        text = requests.get(url)
        dict_ = xmltodict.parse(text.text)
       
        title = dict_['object']['item']['title']
        author = dict_['object']['item']['author']
        price = dict_['object']['item']['priceStandard']
        isbn = dict_['object']['item']['isbn']
        
        books = models.book_info.objects.create(
            title = title,
            author = author,
            price = price,
            isbn = isbn,
        )
        
        return render(request, 'index.html')
        
        
# 찜 목록 리스트 출력하기 
# 1. 리스트를 읽어오기 
# 2. 리스트를 띄울 페이지 생성
# 3. 리스트 순서대로 10개씩 띄우기

def show_book_list(request):
    title = models.book_info.objects.all().order_by('title')
    author = models.book_info.objects.all().order_by('author')
    price = models.book_info.objects.all().order_by('price')
    isbn = models.book_info.objects.all().order_by('isbn')
    context = {}
    context["show_book_list"] = title
    context["show_book_list"] = author
    context["show_book_list"] = price
    context["show_book_list"] = isbn
    
    return render(request, 'show_book_list.html', context)
    
            
            
def register(request):
    
    return render(request, 'register.html')
    
        

def login(request):
    
    return render(request, 'login.html')

    
  
        
        
    
    
    
    
    


