# Generated by Django 4.0.5 on 2022-08-16 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maqari', '0007_alter_hourlyenrollment_enrollment_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hourlyenrollment',
            name='enrollment_number',
            field=models.PositiveIntegerField(default=416171, unique=True),
        ),
        migrations.AlterField(
            model_name='hourlyenrollment',
            name='hours_left',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='hourlyenrollment',
            name='total_hours',
            field=models.PositiveIntegerField(),
        ),
    ]
