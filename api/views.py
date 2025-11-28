from django.shortcuts import render
from django.http import JsonResponse
from .models import Student
# Create your views here.
def studentview(request):
    students=Student.objects.all()
    student_list=list(students.values())
    return JsonResponse(student_list,safe=False)