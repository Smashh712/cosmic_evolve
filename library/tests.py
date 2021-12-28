from django.test import TestCase

# Create your tests here.
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
