# Generated by Django 3.1.5 on 2021-01-25 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffing', '0008_auto_20210124_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
    ]