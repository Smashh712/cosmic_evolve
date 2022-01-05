from django.db import models
from django.utils import timezone
from accounts.models import MyUserManager, MyUser
# Create your models here.


class BookInfomation(models.Model):
    # 도서 정보
    title = models.CharField("도서명", max_length=150) # 도서명
    author = models.CharField("저자", max_length=50) # 저자
    publisher = models.CharField("출판사", max_length=100) # 출판사
    ISBN13 = models.CharField("ISBN13", max_length=13) # ISBN13 13자리 숫자
    ISBN = models.CharField("ISBN", max_length=25) # ISBN ItemType=ItemId, 
    price = models.CharField("가격", max_length=100) # priceStandard
    cover = models.CharField("이미지", max_length=100) # 이미지 
    rentUser = models.CharField("대여자", max_length=100) # 대여자
    startRent = models.DateTimeField(timezone.now()) # 대여 시작일
    rentStatus = models.CharField("대여상태", max_length=30) # 대여상태
    comment = models.TextField("비고") #비고
    
    
class Comment(models.Model):
    # 책에 대한 댓글 
    bookId = models.IntegerField("책ID") # 책ID
    userId = models.CharField("유저ID", max_length=100) # 유저ID
    createDate = models.DateTimeField(timezone.now()) # 작성일
    comment = models.CharField("내용", max_length=250) # 내용
    





    

    
    
    
    