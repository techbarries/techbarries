# Generated by Django 4.0.3 on 2022-03-30 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_alter_event_coverphoto_alter_eventimage_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user_event', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='university',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user_uni', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='venue',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user_venue', to=settings.AUTH_USER_MODEL),
        ),
    ]
