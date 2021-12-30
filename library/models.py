from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta, date
from django.contrib.auth.models import User
# Create your models here.

class book_info(models.Model):
    #도서 정보
    title = models.CharField("도서명", max_length=150)
    author = models.CharField("저자", max_length=50)
    isbn = models.CharField("ISBN", max_length=25) 
    publisher = models.CharField("출판사",max_length=150)
    
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)


        
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True)
    
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True)
    
    





    



        
    
    
    
        
