# Generated by Django 4.0.5 on 2022-07-30 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maqari', '0002_alter_halaqa_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='halaqa',
            name='halaqa_image_url',
            field=models.URLField(default='https://live.staticflickr.com/2139/2435364735_dc51a11e83.jpg'),
        ),
    ]
