# Generated by Django 5.0.1 on 2024-01-22 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0002_map_character_map_cell_id_character__map'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='map',
            name='dofus_id',
        ),
    ]