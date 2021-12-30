from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import requests
import xmltodict
from . import models
from .models import book_info, Answer, Question
from django.core.paginator import Paginator
from .forms import QuestionForm, AnswerForm, BookForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse


def search(request):
    

    keyword = request.POST.get("user_input")
    isbn = request.POST.get('isbn')
    list_ = []
    #f"https://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query={keyword}&QueryType=Title&MaxResults=10&start=1&SearchTarget=Book&output=xml&ItemIdType=ItemId&Version=20070901&Sort=Accuracy&ItemId={isbn}"
    context = {}
    url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query={keyword}&QueryType=title&MaxResults=10&start=1&SearchTarget=Book&output=xml&Version=20070901&Sort=Accuracy&ItemId={isbn}"
    temp = requests.get(url)
    dict_type = xmltodict.parse(temp.text)
    if "item" not in dict_type['object'] :
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
    
    page = request.GET.get('page', '1')
    title = models.book_info.objects.all().order_by('title')
    author = models.book_info.objects.all().order_by('author')
    book_list = [title, author]
    paginator = Paginator(book_list, 10)
    page_obj = paginator.get_page(page)
    context["book_list"] = page_obj
    return render(request, 'index.html', context)
        

@login_required(login_url="common:login")
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
@login_required(login_url="common:login")
def book_add(request):
    # 책 추가하기 
    # 책의 isbn으로 추가하기 name이 isbn인 버튼을 클릭시 objects.create 발동
    
    if request.method == 'POST':
        book = book_info() # 모델에서 도서정보 인스턴스 받아오기
        isbn = request.POST.get('isbn') # 해당 책 정보 얻어오기 위해 isbn을 대푯값으로 설정
        url = f" http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx?ttbkey=ttbmlboy101516001&ItemIdType=ItemId&ItemId={isbn}&output=xml" #알라딘 api로 도서정보 추출
        temp = requests.get(url) #xml파일 추출
        dict_ = xmltodict.parse(temp.text) # 딕셔너리로 파싱
        book.title = dict_['object']['item']['title'] # 제목 추출
        book.author = dict_['object']['item']['author'] # 저자 추출
        book.isbn = dict_['object']['item']['isbn'] # isbn 추출
        book.publisher = dict_['object']['item']['publisher'] # 출판사 추출
        book.user = request.user # 버튼 누른 유저가 그 책을 찜함
        book.save() # 모든 정보 저장
        return redirect('library:search') # 함수종료
    else: # GET이라면
        book = book_info.objects.all() # 도서 객체의 모든 정보 받아와서
        context = {'book': book} # context에 담고
        return render(request, 'index.html', context) #렌더링
        
        
        
# 찜 목록 리스트 출력하기 
# 1. 리스트를 읽어오기 
# 2. 리스트를 띄울 페이지 생성
# 3. 리스트 순서대로 10개씩 띄우기
@login_required(login_url="common:login")
def show_book_list(request):
    if request.method == 'POST':
        title = models.book_info.objects.all().order_by('title')
        author = models.book_info.objects.all().order_by('author')
        publisher = models.book_info.objects.all().order_by('publisher')
        isbn = models.book_info.objects.all().order_by('isbn')
        user = models.book_info.objects.all().order_by('user')
        context = {}
        context["show_book_list"] = title
        context["show_book_list"] = author
        context["show_book_list"] = publisher
        context["show_book_list"] = isbn
        context["show_book_list"] = user
        return render(request, 'show_book_list.html', context)
    else: 
        books = models.book_info.objects.all()
        context = {'show_book_list': books}
        return render(request, 'show_book_list.html', context)
        
    
            


    
# 자유게시판 관련 함수들 ###
def index(request):
    '''
    목록 출력
    '''
    page = request.GET.get('page', '1') # 페이지 가져오기
    
    question_list = Question.objects.all().order_by('-create_date') # 조회
    
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    ## Paginator 클래스는 페이징 구현 클래스
    return render(request, 'question_list.html', context)


def detail_index(request, question_id):
    '''
    내용 출력
    '''
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'question_detail.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    '''
    댓글 등록
    '''
    
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('library:detail_index', question_id = question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}

    return render(request, 'question_detail.html', context)
    
# 이 폼에 도서 등록하기 참고
# 글을 작성하고 질문 등록하기 버튼을 누르면 POST 방식으로 작동되고
# 글을 작성하지 않으면 else가 실행되어 GET 방식으로 url을 요청한다.
#form.save(commit=False)이 함수가 모델 데이터 저장 함수
# commit=False는 임시저장 이유는 create_date가 아직 forms에 없기 때매
# create_date는 함수 내에서 자체적으로 timezone.now()를 이용해 현재시간을
#저장한다.
#그 후 저장한 데이터들을 question.save()로 데이터에 실제로 저장
@login_required(login_url='common:login')
def question_create(request):
    '''
    글 작성
    '''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('library:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'question_form.html', context)

    
# def wishlist(request):
#     '''
#     책 등
#     '''

@login_required(login_url='common:login')
def question_modify(request, question_id):
    '''
    글 수정
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('library:detail', question_id=question.id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('library:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'question_form.html',context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect('library:detail', question_id=question.id)
    question.delete()
    return redirect('library:question_list')