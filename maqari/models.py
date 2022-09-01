from django.db import models
from django.forms import BooleanField, CharField, DateTimeField
from account.models import Account
import uuid
# Create your models here.

class HalaqaType(models.Model):
    type_name = models.CharField(max_length=100)
    type_desc = models.TextField(max_length = 500)

    def __str__(self):
        return str(self.type_name)

    def serialize(self):
        return{
            'type_name' : self.type_name,
            'type_desc' : self.type_desc,
        }

class Halaqa(models.Model):

    Genders=[
        ("Male","Male"),
        ("Female","Female")
    ]

    halaqa_number = models.IntegerField(unique=True)
    gender = models.CharField(max_length=7,choices=Genders,default = "Male")
    timings = models.TextField(max_length=100,blank=True)
    teacher = models.ForeignKey(Account, null = True, on_delete=models.SET_NULL,related_name="teacher_in_halaqaat")
    students = models.ManyToManyField(Account,blank=True,related_name="students_halaqa")
    supervisor = models.ForeignKey(Account, null = True, on_delete=models.SET_NULL, related_name="supervised_halaqaat")
    halaqa_type = models.ForeignKey(HalaqaType,null=True,on_delete=models.SET_NULL,related_name="halaqaat_of_type")
    halaqa_image_url = models.URLField(default='https://live.staticflickr.com/2139/2435364735_dc51a11e83.jpg')

    def __str__(self):
        return str(self.halaqa_number)

    def serialize(self):
        if self.halaqa_type:
            type = self.halaqa_type.serialize()
        else:
            type = None
        
        self_teacher = self.teacher
        self_supervisor = self.supervisor

        return{
            'halaqa_id' : self.id,
            'halaqa_number' : self.halaqa_number,
            'gender' : self.gender,
            'timings' : self.timings,
            'teacher_id' : self_teacher.id,
            'teacher_name' : f"{self_teacher.username} {self_teacher.last_name}",
            'teacher_profile': self_teacher.profile_image,
            'teacher_years_of_experience':self_teacher.years_of_experience,
            'teacher_current_residence' : self_teacher.current_residence.name,
            'teacher_nationality' : self_teacher.nationality.name,
            'supervisor_id' : self_supervisor.id,
            'supervisor_name' : f"{self_supervisor.username} {self_supervisor.last_name}",
            'halaqa_type' : type,
            'halaqa_image_url' : self.halaqa_image_url,
            'student_count':self.students.count()
        }

class HourlyEnrollment(models.Model):
    enrollment_number = models.UUIDField(primary_key = True,default=uuid.uuid4,editable=False)
    student = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL, related_name="student_hourly_enrollments")
    total_hours = models.PositiveIntegerField()
    hours_left = models.PositiveIntegerField()
    enrollment_type = models.ForeignKey(HalaqaType,null=True,on_delete=models.SET_NULL,related_name="enrollments_of_type")

    def __str__(self):
        return str(str(self.enrollment_number) + ' - ' + str(self.student))

class ExamType(models.Model):
    type_name = models.CharField(max_length=100)
    type_desc = models.TextField(max_length=500)
    is_open = models.BooleanField(default=False)
    total_marks = models.IntegerField()
    hifdh_marks = models.IntegerField(blank=True , null=True)
    tajweed_marks = models.IntegerField(blank=True , null=True)    

    def __str__(self):
        return self.type_name
    
class Exam(models.Model):
    
    ratings=[
        ("Excellent","Excellent"),
        ("Very_Good","Very Good"),
        ("Good","Good"),
        ("Fail","Fail"),
        ("Absent","Absent"),
        ("Pending","Pending"),
    ]

    student = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL, related_name="student_exams")
    halaqa = models.ForeignKey(Halaqa,null=True,on_delete=models.SET_NULL,related_name="halaqa_exams")
    exam_type = models.ForeignKey(ExamType, null=True, on_delete=models.SET_NULL, related_name="exams_of_type")
    exam_halaqah_type = models.ForeignKey(HalaqaType,null=True,on_delete=models.SET_NULL,related_name="exams_of_halaqa_type")
    exam_date = models.DateField(null=True,blank=True)
    exam_year = models.IntegerField(null = True,blank=True)
    exam_timing = models.TextField(max_length=100)

    exam_from = models.CharField(max_length=50,null=True)
    exam_till = models.CharField(max_length=50,null=True)
    number_of_juz = models.FloatField(null=True)

    is_completed = models.BooleanField(default=False)
    examiner1 = models.ForeignKey(Account, blank=True,null=True, on_delete=models.PROTECT,related_name="Examiner1_exams")
    examiner2 = models.ForeignKey(Account, blank=True,null=True, on_delete=models.PROTECT,related_name="Examiner2_exams")
    rating = models.CharField(choices=ratings,max_length=50,default="Pending")
    total_marks_obtained = models.FloatField(blank=True,null=True)
    hifdh_marks_obtained = models.FloatField(blank=True,null=True)
    tajweed_marks_obtained = models.FloatField(blank=True,null=True)

    def __str__(self):
        return f"{self.student.username} {self.student.last_name} - {self.exam_type.type_name} - {self.number_of_juz} juz - {self.exam_date}"

    class Meta:
        unique_together = ('student','exam_type','exam_halaqah_type')

class Stats(models.Model):

    taqdeer = [
        ("Excellent","Excellent"),
        ("Very Good","Very Good"),
        ("Good","Good"),
        ("Not Acceptable","Not Acceptable"),
        ("Not Recited","Not Recited"),
    ]

    attendance_choices = [
        ("Present","Present"),
        ("Absent","Absent"),
        ("Late","Late"),
    ]

    account = models.ForeignKey(Account,null=True,on_delete=models.SET_NULL,related_name="account_stats")
    halaqa = models.ForeignKey(Halaqa,null=True,on_delete=models.SET_NULL,related_name="halaqa_student_stats")
    date = models.DateField()
    attendance = models.CharField(max_length=10,choices=attendance_choices,default="Absent")
    dars = models.CharField(max_length=50,blank=True,default="none")
    dars_pages = models.FloatField(blank=True,default=0)
    taqdeer_dars = models.CharField(max_length=20, choices=taqdeer,default="Not Recited")
    murajia = models.CharField(max_length=100,blank=True,default="none")
    murajia_pages = models.IntegerField(blank=True,default=0)
    taqdeer_murajia = models.CharField(max_length=20, choices=taqdeer,default="Not Recited")

    class Meta:
        unique_together = ('account','halaqa','date')

    def __str__(self):
        return str(str(self.date) + str(self.account))