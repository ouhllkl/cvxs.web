# Generated by Django 3.2.12 on 2023-04-28 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20230428_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='administration_profile',
            name='change_current_procedures',
            field=models.BooleanField(default=1),
        ),
    ]
