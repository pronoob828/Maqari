from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from maqari.models import Halaqa,Stats
from account.models import Account
from maqari.forms import StatForm


# Create your views here.

def index(request):
    return render(request,"maqari/index.html")

def show_your_classes(request):
    user = request.user
    enrolled_halaqaat = Halaqa.objects.filter(students = user)
    serialized_data = [halaqa.serialize() for halaqa in enrolled_halaqaat]
    for halaqa in serialized_data:
        halaqa["is_enrolled"] = True
    return render(request,"maqari/your_classes.html",{
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

def show_supervised_classes(request):
    user = request.user
    halaqaat = Halaqa.objects.filter(supervisor = user).order_by("halaqa_number")
    serialized_data = [halaqa.serialize() for halaqa in halaqaat]
    for halaqa in serialized_data:
        if user in Halaqa.objects.get(halaqa_number = halaqa['halaqa_number']).students.all():
            halaqa["is_enrolled"] = True
    return render(request,"maqari/supervised_classes.html",{
        'halaqaat' : serialized_data
    })

def show_taught_classes(request):
    user = request.user
    taught_halaqaat = Halaqa.objects.filter(teacher = user)
    serialized_data = [halaqa.serialize() for halaqa in taught_halaqaat]
    for halaqa in serialized_data:
        halaqa["is_enrolled"] = True
    return render(request,"maqari/classes_taught.html",{
        'halaqaat' : serialized_data
    })

def show_halaqa(request,halaqa_id):
    halaqa = Halaqa.objects.get(id = halaqa_id)
    return render(request,"maqari/halaqa.html",{'halaqa':halaqa})

def render_student_search(request):
    if request.POST:
        context = {}
        data = request.POST
        query = data["query"]
        subordinate_ids = request.user.get_subordinates()
        dataset = Account.objects.filter(id__in = subordinate_ids)
        results = []
        results += (dataset.filter(username = query).all()|dataset.filter(last_name = query).all()|dataset.filter(phone_num = query).all())
        results += (dataset.filter(email__icontains = query).all()|dataset.filter(username__icontains = query).all()|dataset.filter(last_name__icontains = query).all())
        context['results'] = results
        print(results)
        return render(request,"maqari/student_search.html",context)    
    return render(request,"maqari/student_search.html")

def add_student_stats(request):
    if not request.user.is_authenticated:
        return HttpResponse("Need login",status = 403)
    
    if request.POST:
        form = StatForm(request.POST)
        if form.is_valid:
            data = request.POST
            account = Account.objects.get(id = data['account'])
            halaqa = Halaqa.objects.get(id = data['halaqa'])
            date = data['date']
            attendance = data['attendance']
            dars = data['dars']
            try:
                dars_pages = float(data['dars_pages'])
            except:
                dars_pages = 0
            taqdeer_dars = data['taqdeer_dars']
            murajia = data['murajia']
            try:
                murajia_pages = int(data['murajia_pages'])
            except:
                murajia_pages = 0
            taqdeer_murajia = data['taqdeer_murajia']

            if request.user == halaqa.teacher or request.user.is_superuser:
                if attendance == "Absent":
                    dars = "none"
                    dars_pages = 0
                    taqdeer_dars = "Not Recited"
                    murajia = "none"
                    murajia_pages = 0
                    taqdeer_murajia = "Not Recited"

                try:
                    new_stat = Stats(account = account,halaqa=halaqa,date=date,attendance=attendance,dars = dars,dars_pages=dars_pages,taqdeer_dars=taqdeer_dars,murajia=murajia,murajia_pages=murajia_pages,taqdeer_murajia=taqdeer_murajia)
                    new_stat.save()
                except IntegrityError:
                    return HttpResponseRedirect(reverse("show_profile",kwargs = {'user_id':account.id}))
                return HttpResponseRedirect(reverse("show_profile",kwargs = {'user_id':account.id}))
            else:
                return HttpResponse("Only teachers can add their student's stats")


