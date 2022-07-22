# Generated by Django 4.0.3 on 2022-07-22 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_rename_popular_venue_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='reminder_sent',
            field=models.BooleanField(blank=True, default=False, help_text='Designates whether the event reminder sent to users.', verbose_name='Event reminder sent'),
        ),
    ]
