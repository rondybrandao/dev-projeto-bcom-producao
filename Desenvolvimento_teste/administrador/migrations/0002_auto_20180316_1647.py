# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-16 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controle_despesas',
            name='qnt_combustivel',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]