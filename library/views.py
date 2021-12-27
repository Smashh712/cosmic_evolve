from django.shortcuts import render,redirect
from library.models import Student
import requests
import xmltodict
import json

# Create your views here.

# def submit(request):
#     name_ =request.POST.get('name')
#     if(name_):
#         age_ = request.POST.get('age')
#         sex_ = request.POST.get('sex')
        
#         Student.objects.create(
#             name = name_,
#             age = age_,
#             sex = sex_,
#         )
    
#     students = []
#     for student in Student.objects.all():
#         temp = []
#         temp.append(student.name)
#         temp.append(student.age)
#         temp.append(student.sex)
#         students.append(temp)
#     #print(students)
#     #print(Student.objects.all()[0].name)
#     context = {}    
    
    
#     context["students"] = students
    
#     return render(request, 'index.html',context)


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
        url = f" http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey=ttbmlboy101516001&Query=Title&QueryType=Title&MaxResults=10&start=1&SearchTarget=Book&output=xml&Version=20070901&ItemIdType=ItemId&ItemId={isbn}"
        test = requests.get(url)
        dict_type = xmltodict.parse(test.text)
        title = dict_type["object"]['item']['title']
        author = dict_type['object']['item']['author']
        picture = dict_type['object']['item']['cover']
        
        list_ = [title, author, picture]
        context = {}
        
        context["detail"] = list_
        
        return render(request, 'detail.html', context)
    
    else:
        return render(request, 'detail.html')
        
    