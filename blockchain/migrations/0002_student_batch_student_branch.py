# Generated by Django 5.0.6 on 2024-11-28 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='batch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='branch',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
