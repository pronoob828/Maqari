import http
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from maqari.models import ExamType, Halaqa, HourlyEnrollment,Stats,Exam,HalaqaType
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

halaqaat_to_be_displayed_on_one_page = 10

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
        if user in halaqa.students.all() or user==halaqa.teacher or user==halaqa.supervisor:
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

def show_exams(request):
    user = request.user
    user_students = Account.objects.filter(id__in = user.get_subordinates())
    context = {}
    context['active_exams'] = Exam.objects.filter(student__in = user_students, is_completed = False)
    if request.POST:
        data = request.POST
        try:
            student = Account.objects.get(email = data['student'])
        except:
            return HttpResponse("Invalid Student")
        try:
            halaqa = Halaqa.objects.get(halaqa_number = data["halaqa"])
        except:
            return HttpResponse("Invalid Halaqa")
        try:
            exam_type = ExamType.objects.get(type_name = data["exam_type"])
        except:
            return HttpResponse("Invalid Exam Type")
        exam_timing = data["exam_timing"]
        exam_from = data["exam_from"]
        exam_till = data["exam_till"]
        number_of_juz = data["number_of_juz"]
        exam_halaqa_type = halaqa.halaqa_type


        if student in halaqa.students.all():
            try:
                new_exam = Exam(student=student,halaqa=halaqa,exam_type=exam_type,exam_timing=exam_timing,exam_from=exam_from,exam_till=exam_till,number_of_juz=number_of_juz,exam_halaqah_type=exam_halaqa_type)
                new_exam.save()
                return redirect("show_exams")
            except:
                return HttpResponse("Something went wrong",status=500)
        else:
            return HttpResponse("Invalid data",status=403)
    else:

        # GET request

        context['students'] = Account.objects.filter(id__in = user.get_students())
        context['halaqaat'] = Halaqa.objects.filter(teacher = user)
        context['exam_type'] = ExamType.objects.filter(is_open = True)
    return render(request, "maqari/exams.html",context)

def show_exam_details(request,exam_id):
    exam = Exam.objects.get(id = exam_id)
    user = request.user
    if not (user == exam.halaqa.teacher or user == exam.halaqa.supervisor or user == exam.student):
        return HttpResponse("You are not authorized to view this page", status=403)

    context = {}
    context['exam'] = exam
    context['pass_ratings'] = ['Excellent','Very Good','Good']
    context['fail_ratings'] = ['Fail','Absent','Pending']
    if request.user == exam.halaqa.teacher or request.user == exam.halaqa.supervisor:
        context['teacher_view'] = True
    else:
        context['teacher_view'] = False 
    return render(request,"maqari/exam_details.html",context)

def cancel_exam(request):
    if request.POST:
        data = request.POST
        exam_id = data["exam_id"]
        exam = Exam.objects.get(id=exam_id)
        if request.user == exam.halaqa.teacher or request.user == exam.halaqa.supervisor:
            exam.delete()
        else:
            return HttpResponse("Permission Denied",status=403)
        return redirect("show_exams")
    else:
        return HttpResponse("Invalid Access Method",status=403)

def enroll_student(request,halaqa_id):
    halaqa = Halaqa.objects.get(id = halaqa_id)
    halaqa.students.add(request.user)
    return redirect("show_halaqa",halaqa_id)
    
def show_hourly_enrollment(request,enrollment_number):
    enrollment = HourlyEnrollment.objects.get(enrollment_number = enrollment_number)
    student = enrollment.student
    context = {}
    if request.user.is_authenticated and (request.user.is_teacher or request.user.is_superuser or request.user.is_supervisor or request.user == student):
         context['enrollment'] = enrollment
         return render(request,'maqari/enrollment.html',context)
    else:
        return HttpResponse("Permission Denied",status = 403)

def enrollments_page(request):
    context = {}
    if request.POST:
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        data = request.POST
        student = request.user
        total_hours = data['total_hours']
        enrollment_type = HalaqaType.objects.get(type_name = data['type'])
        new_enrollment = HourlyEnrollment(student=student,total_hours=total_hours,enrollment_type=enrollment_type,hours_left=total_hours)
        new_enrollment.save()
        return redirect(reverse('show_profile',kwargs={'user_id':request.user.id}))
    
    context['types'] = HalaqaType.objects.all()
    return render(request,"maqari/enrollments_page.html",context)

def search_enrollment(request):
    user = request.user
    context = {}
    context['types'] = HalaqaType.objects.all()
    if request.POST:
        if user.is_authenticated:
            if user.is_staff or user.is_superuser or user.is_teacher or user.is_supervisor:
                data = request.POST
                query = data['query']
                dataset = HourlyEnrollment.objects.filter(hours_left__gt = 0)
                results = []
                try:
                    results += dataset.filter(enrollment_number = query)
                    if results != []:
                        context = {}
                        context['enrollment'] = results[0]
                        return render(request,'maqari/enrollment.html',context)
                except:
                    pass
                spaced = query.split(' ')
                results += dataset.filter(student__username__in = spaced, student__last_name__in = spaced).all()
                results += dataset.filter(student__username = query).all() | dataset.filter(student__last_name = query).all() | dataset.filter(student__email = query).all()
                results += dataset.filter(enrollment_type__type_name__iexact = query).all() | dataset.filter(student__username__icontains = query).all() | dataset.filter(student__last_name__icontains=query).all() | dataset.filter(student__email__icontains = query).all()
                context['results'] = set(results)
                return render(request,"maqari/enrollments_page.html",context)
            else:
                return HttpResponse("Permission Denied",status=403)
        else:
            return redirect(reverse("login"))
    else:
        return render(request,"maqari/enrollments_page.html",context)
