# Generated by Django 4.0.3 on 2022-07-08 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtransaction',
            name='currency',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='eventtransaction',
            name='payment_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
