# Generated by Django 5.0.6 on 2024-11-29 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0006_student_sid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='last_otp_generated',
        ),
        migrations.RemoveField(
            model_name='student',
            name='otp',
        ),
    ]
