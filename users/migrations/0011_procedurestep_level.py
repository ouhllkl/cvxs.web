# Generated by Django 3.2.12 on 2023-04-27 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_procedure_procedurestep'),
    ]

    operations = [
        migrations.AddField(
            model_name='procedurestep',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
