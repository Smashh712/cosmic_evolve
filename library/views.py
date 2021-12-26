from django.shortcuts import render

# Create your views here.

def submit(request):
    context = request.POST
    return render(request, 'index.html',context)

