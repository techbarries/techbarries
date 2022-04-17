# Generated by Django 4.0.3 on 2022-04-17 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0008_remove_event_coverphoto_event_cover_photo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hosted', models.BooleanField(blank=True, default=0, null=True)),
                ('checked_in', models.BooleanField(blank=True, default=0, null=True)),
                ('pinned', models.BooleanField(blank=True, default=0, null=True)),
                ('paid', models.BooleanField(blank=True, default=0, null=True)),
                ('guest_list', models.BooleanField(blank=True, default=0, null=True)),
                ('invited', models.BooleanField(blank=True, default=0, null=True)),
                ('public', models.BooleanField(blank=True, default=0, null=True)),
                ('not_going', models.BooleanField(blank=True, default=0, null=True)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_status', to='events.event')),
                ('user_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_event_interaction', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
