# Generated by Django 4.0.5 on 2022-07-30 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_account_role_of_account'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Role',
        ),
    ]