from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    age = models.IntegerField("나이")
    name = models.CharField("이름", max_length=20)
    sex = models.CharField("성별", max_length=20)
    
    
    
    


        
    
        
        
        
