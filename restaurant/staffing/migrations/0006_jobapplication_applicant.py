# Generated by Django 3.1.5 on 2021-01-24 01:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staffing', '0005_remove_jobapplication_applicant'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='applicant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
