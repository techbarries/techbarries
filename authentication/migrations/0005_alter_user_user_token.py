# Generated by Django 4.0.3 on 2022-04-02 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_university'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_token',
            field=models.TextField(blank=True, default=None, verbose_name='user token'),
        ),
    ]
