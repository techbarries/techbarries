# Generated by Django 4.0.3 on 2022-04-05 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_user_user_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_token',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='user token'),
        ),
    ]
