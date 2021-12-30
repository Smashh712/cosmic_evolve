from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from library.models import Answer, Question, book_info
from library.models import Question

class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')
    
    class Meta:
        model = User
        fields = ("username", 'email')
        

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']

        labels = {
            'subject': '제목',
            'content': '내용',
        }
        
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }
        

class BookForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = book_info
        fields = '__all__'
        