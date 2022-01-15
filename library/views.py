from django.core import paginator
from django.shortcuts import render
from accounts import models
from . import models
import requests
import xmltodict
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import time
from django.core.paginator import Paginator
from accounts.models import MyUser
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


# 소장도서들 출력
def index(request):
    books = models.BookInfomation.objects.all().order_by("title")
    context = {}
    page = request.GET.get("page", "1")
    paginator = Paginator(books, 10)
    page_obj = paginator.get_page(page)
    context["is_staff"] = request.user.is_staff
    context["book"] = page_obj
    if str(request.user) == "AnonymousUser":
        print(request.user)
        context["username"] = "AnonymousUser"
    else:
        context["username"] = str(request.user.name)
    return render(request, "index.html", context)


# 메인페이지
def home(request):
    return render(request, "home.html")


# 소장도서 추가
# 어드민 권한 부여 요구
@login_required
def bookAdd(request):
    if request.method == "POST":
        book = models.BookInfomation()  # db에서 책 정보 가져오기
        isbn = request.POST.get("ISBN")
        url = f" http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey=ttbmlboy101516001&ItemIdType=ISBN&ItemId={isbn}&output=xml"  # 알라딘 api로 도서정보 추출
        temp = requests.get(url)
        result = xmltodict.parse(temp.text)
        book.title = result["object"]["item"]["title"]
        book.author = result["object"]["item"]["author"]
        book.publisher = result["object"]["item"]["publisher"]
        book.ISBN13 = result["object"]["item"]["isbn13"]
        book.ISBN = result["object"]["item"]["isbn"]
        book.price = result["object"]["item"]["priceStandard"]
        book.cover = result["object"]["item"]["cover"]
        book.rentUser = "없음"
        book.startRent = timezone.now()
        book.rentStatus = "소장중"
        book.save()
        return redirect("library:index")

    else:
        book = models.BookInfomation.objects.all()
        context = {"book": book}
        return render(request, "index.html", context)


# 베스트 셀러들 출력
def printBooks(request):
    url = "http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=ttbmlboy101516001&QueryType=Bestseller&MaxResults=10&start=1&SearchTarget=Book&output=xml&Version=20131101"
    temp = requests.get(url)
    result = xmltodict.parse(temp.text)
    page = request.GET.get('page', '1')
    list_ = []
    for i in range(10):
        title = result["object"]["item"][i]["title"]
        author = result["object"]["item"][i]["author"]
        publisher = result["object"]["item"][i]["publisher"]
        cover = result["object"]["item"][i]["cover"]
        description = result["object"]["item"][i]["description"]
        isbn = result["object"]["item"][i]["isbn"]
        list_.append([title, author, publisher, cover, description, isbn])
    
    paginator = Paginator(list_, 10)
    page_obj = paginator.get_page(page)
    context = {}
    context["is_staff"] = request.user.is_staff
    context["book"] = page_obj
    return render(request, "showbooks.html", context)


# 소장도서 소중단에 반납 기능
### 어드민만 반납할 수 있게 구현 요구 ###
@login_required
def returnBook(request):
    bookid = request.POST.get("bookid")
    book = models.BookInfomation.objects.get(id=bookid)
    if int(bookid) == book.id:
        book.delete()
        return redirect("library:index")
    else:
        return redirect("library:index")


# 검색 기능
def search(request):
    keyword = request.POST.get("user_input")
    isbn = request.POST.get("ISBN")
    list_ = []
    context = {}
    url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query={keyword}&QueryType=title&MaxResults=10&start=1&SearchTarget=Book&output=xml&Version=20070901&Sort=Accuracy&ItemId={isbn}"
    temp = requests.get(url)
    result = xmltodict.parse(temp.text)
    if "item" not in result["object"]:
        list_ = [["검색결과가 존재하지 않습니다", None, None]]
    else:
        for i in range(len(result["object"]["item"])):
            if len(result["object"]["item"]) == 18:
                title = result["object"]["item"]["title"]
                author = result["object"]["item"]["author"]
                publisher = result["object"]["item"]["publisher"]
                cover = result["object"]["item"]["cover"]
                ISBN = result["object"]["item"]["isbn"]
                list_.append([title, author, publisher, cover, ISBN])
                break
            else:
                title = result["object"]["item"][i]["title"]
                author = result["object"]["item"][i]["author"]
                publisher = result["object"]["item"][i]["publisher"]
                cover = result["object"]["item"][i]["cover"]
                ISBN = result["object"]["item"][i]["isbn"]
                list_.append([title, author, publisher, cover, ISBN])

    context["book"] = list_
    page = request.GET.get("page", "1")
    paginator = Paginator(list_, 10)
    page_obj = paginator.get_page(page)
    context["bookList"] = page_obj
    context["is_staff"] = request.user.is_staff
    return render(request, "resultAladinSearch.html", context)


# 상세정보 띄우기
def detail(request):
    isbn = request.POST.get("ISBN")

    if isbn:
        url = f" http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey=ttbmlboy101516001&ItemIdType=ISBN&ItemId={isbn}&output=xml"

        test = requests.get(url)
        dict_type = xmltodict.parse(test.text)

        title = dict_type["object"]["item"]["title"]
        author = dict_type["object"]["item"]["author"]
        picture = dict_type["object"]["item"]["cover"]
        price = dict_type["object"]["item"]["priceStandard"]
        list_ = [title, author, price, picture]
        context = {}
        context["detail"] = list_
        return render(request, "detail.html", context)

    else:
        return render(request, "index.html")


# 대여 추가 함수
@login_required
def rentBook(request):
    if request.method == "POST":
        bookid = request.POST.get("bookid")
        book = models.BookInfomation.objects.get(id=bookid)  # db에서 책 정보 가져오기
        book.rentUser = str(request.user)
        book.rentStatus = "대출 중"
        book.save()

        return redirect("library:index")

    else:
        book = models.BookInfomation.objects.all()
        context = {"book": book}
        return render(request, "index.html", context)


# 대출한 도서 반납 함수
@login_required
def rentalReturnBook(request):
    # rentUser = request.POST.get('rentUser')
    bookid = request.POST.get("bookid")
    book = models.BookInfomation.objects.get(id=bookid)
    if str(request.user) == str(book.rentUser):
        book.rentStatus = "소장중"
        book.rentUser = "없음"
        book.save()
        return redirect("library:index")
    else:
        return redirect("library:index")

    # #bookid = request.POST.get('bookid')
    # book = models.BookInfomation.objects.get(id=bookid)
    # if int(bookid) == book.id:
    #     book.delete()
    #     return redirect('library:index')
    # else:
    #     return redirect('library:index')



@login_required
def myBookList(request):
        rentUser = str(request.user)
        bookList = models.BookInfomation.objects.filter(rentUser=rentUser)
        context = {}
        context['bookList'] = bookList
        return render(request, 'myBookList.html', context)


### bookAdd 함수 어드민만 반납할 수 있게 구현 요구 ###
### 책 빌리기 함수 수정하기 요구###
###rentStatus 페이지 필요없을 듯###
###about 페이지 구현###
