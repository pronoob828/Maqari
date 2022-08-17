# Generated by Django 4.0.5 on 2022-08-17 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maqari', '0013_alter_hourlyenrollment_enrollment_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='halaqa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='halaqa_exams', to='maqari.halaqa'),
        ),
        migrations.AlterField(
            model_name='hourlyenrollment',
            name='enrollment_number',
            field=models.PositiveIntegerField(default=180121, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='exam',
            unique_together={('student', 'exam_type', 'exam_halaqah_type')},
        ),
    ]