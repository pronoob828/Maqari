# Generated by Django 4.0.5 on 2022-07-30 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_account_user_permissions_alter_account_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='role_of_account',
        ),
    ]