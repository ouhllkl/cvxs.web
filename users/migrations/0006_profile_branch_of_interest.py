# Generated by Django 3.2.12 on 2023-04-24 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230423_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='branch_of_interest',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
