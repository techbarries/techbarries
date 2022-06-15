# Generated by Django 4.0.3 on 2022-06-15 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='latitude',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='longitude',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
    ]
