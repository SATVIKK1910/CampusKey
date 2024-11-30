# Generated by Django 5.0.6 on 2024-11-28 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0002_student_batch_student_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='otp',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='secure_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
