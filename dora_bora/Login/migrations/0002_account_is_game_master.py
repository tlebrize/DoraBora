# Generated by Django 5.0.1 on 2024-01-19 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_game_master',
            field=models.BooleanField(default=False),
        ),
    ]