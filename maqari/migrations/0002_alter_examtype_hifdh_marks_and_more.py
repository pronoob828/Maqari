# Generated by Django 4.0.5 on 2022-09-01 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maqari', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examtype',
            name='hifdh_marks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='examtype',
            name='tajweed_marks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]