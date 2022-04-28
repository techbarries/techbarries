# Generated by Django 4.0.3 on 2022-04-28 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='description')),
                ('redirect_to', models.CharField(choices=[('EVENT_PAGE', 'EVENT_PAGE'), ('EVENT_GUEST_LIST_PAGE', 'EVENT_GUEST_LIST_PAGE'), ('CHAT_PAGE', 'CHAT_PAGE'), ('FRIEND_PROFILE_PAGE', 'FRIEND_PROFILE_PAGE'), ('MY_WALLET_PAGE', 'MY_WALLET_PAGE'), ('MY_WALLET_TICKET_PAGE', 'MY_WALLET_TICKET_PAGE'), ('REPORT_PAGE', 'REPORT_PAGE')], default='EVENT_PAGE', max_length=100, null=True)),
                ('details', models.TextField(blank=True, default=None, null=True, verbose_name='details')),
                ('status', models.BooleanField(blank=True, default=0, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_created_by_user', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
