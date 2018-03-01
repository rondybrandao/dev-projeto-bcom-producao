# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 06:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dev_radioanori', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='qnt_crianca',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='compra',
            name='viagem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dev_radioanori.Viagem'),
        ),
    ]
