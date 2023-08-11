# Generated by Django 4.2.4 on 2023-08-10 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('partially completed', 'Partially Completed'), ('completed', 'Completed')], default='pending', max_length=30),
        ),
        migrations.AddField(
            model_name='billitem',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
    ]