from django.db import models
# Create your models here.



class book_info(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    isbn = models.CharField(max_length=20)
        
class member(models.Model):
    email = models.EmailField()
    student_number = models.IntegerField()
    password = models.CharField(max_length=40)

        
        
