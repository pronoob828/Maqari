from re import A
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from maqari.models import Halaqa
from account.models import Account


# Create your views here.

def index(request):
    return render(request,"maqari/index.html")

def show_my_classes(request):
    user = request.user
    enrolled_halaqaat = Halaqa.objects.filter(students = user)
    serialized_data = [halaqa.serialize() for halaqa in enrolled_halaqaat]
    return render(request,"maqari/my_classes.html",{
        'data' : serialized_data
    })

def render_available_classes(request):
    return render(request,"maqari/available_classes.html")

def show_available_classes(request,page_no):
    user = request.user
    if user.is_authenticated:
        halaqaat = Paginator(Halaqa.objects.filter(gender = user.gender).order_by("halaqa_number").all(),15)
    else:
        halaqaat = Paginator(Halaqa.objects.all().order_by("halaqa_number").all(),10)

    page = halaqaat.page(page_no).object_list

    serialized_data = [halaqa.serialize() for halaqa in page]
    for halaqa in serialized_data:
        if user.is_authenticated:
            if is_enrolled(user,halaqa['halaqa_id']):
                halaqa["is_enrolled"] = True
            else:
                halaqa["is_enrolled"] = False
        else:
            halaqa["is_enrolled"] = False
    #return render(request,"maqari/available_classes.html", {
        #'data':serialized_data
    #})
    return JsonResponse(serialized_data,safe=False)

def is_enrolled(user, halaqa_id):
    try:
        halaqa = Halaqa.objects.get(id = halaqa_id)
        if user in halaqa.students.all():
            return True
        else:
            return False
    except:
        return False