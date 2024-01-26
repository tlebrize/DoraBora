# Generated by Django 5.0.1 on 2024-01-26 22:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monstergroup',
            name='_map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monster_groups', to='Game.map'),
        ),
        migrations.AlterField(
            model_name='monstergroup',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monster_groups', to='Game.monstergrouptemplate'),
        ),
    ]