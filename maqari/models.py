from django.db import models
from django.forms import CharField, DateTimeField
from account.models import Account

# Create your models here.

class HalaqaType(models.Model):
    type_name = models.CharField(max_length=100)
    type_desc = models.TextField(max_length = 500)

    def __str__(self):
        return self.type_name

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

    def serialize(self):
        if self.halaqa_type:
            type = self.halaqa_type.serialize()
        else:
            type = None
        return{
            'halaqa_id' : self.id,
            'halaqa_number' : self.halaqa_number,
            'gender' : self.gender,
            'timings' : self.timings,
            'teacher_id' : self.teacher.id,
            'teacher_name' : f"{self.teacher.username} {self.teacher.last_name}",
            'supervisor_id' : self.supervisor.id,
            'supervisor_name' : f"{self.supervisor.username} {self.supervisor.last_name}",
            'halaqa_type' : type,
            'halaqa_image_url' : self.halaqa_image_url,
        }

