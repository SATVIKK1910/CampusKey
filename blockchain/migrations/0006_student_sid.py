# Generated by Django 5.0.6 on 2024-11-29 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0005_student_last_otp_generated'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='sid',
            field=models.CharField(default='000000', max_length=15),
        ),
    ]