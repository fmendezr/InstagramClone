# Generated by Django 4.2.3 on 2023-07-21 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(upload_to='profile_imgs/'),
        ),
    ]
