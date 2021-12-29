from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
# Create your models here.

class book_info(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    isbn = models.CharField(max_length=20)
    

        
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    
    





    



        
    
    
    
        
