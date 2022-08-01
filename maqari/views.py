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
    teaching_halaqaat = Halaqa.objects.filter(teacher = user)
    serialized_data = [halaqa.serialize() for halaqa in enrolled_halaqaat]
    serialized_data += [halaqa.serialize() for halaqa in teaching_halaqaat]
    for halaqa in serialized_data:
        halaqa["is_enrolled"] = True
    return render(request,"maqari/my_classes.html",{
        'data' : serialized_data
    })

def render_available_classes(request):
    return render(request,"maqari/available_classes.html")

halaqaat_to_be_displayed_on_one_page = 15

def get_page_count(request):
    halaqaat = Paginator(Halaqa.objects.all().order_by("halaqa_number").all(),halaqaat_to_be_displayed_on_one_page)
    page_count = halaqaat.num_pages
    return JsonResponse({"page_count": page_count})

def show_available_classes(request,page_no):
    user = request.user
    halaqaat = Paginator(Halaqa.objects.all().order_by("halaqa_number").all(),halaqaat_to_be_displayed_on_one_page)

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