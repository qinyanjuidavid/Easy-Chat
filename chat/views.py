from django.shortcuts import render
from django.http import HttpResponse,JsonResponse



def index(request):
    context={

    }
    return render(request,"chat/index.html",context)