# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-25 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev_radioanori', '0003_auto_20180425_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viagem',
            name='preco_crianca',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
