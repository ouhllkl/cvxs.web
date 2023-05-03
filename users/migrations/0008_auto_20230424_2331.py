# Generated by Django 3.2.12 on 2023-04-24 23:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0007_profile_branch_of_interest_degree_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='branch_of_interest_degree_type',
            field=models.CharField(blank=True, choices=[('1', 'Bachelor'), ('2', 'Master'), ('3', 'PHD')], max_length=100),
        ),
        migrations.CreateModel(
            name='administration_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_for_new_applications', models.BooleanField(default=0)),
                ('accept_applications', models.BooleanField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
