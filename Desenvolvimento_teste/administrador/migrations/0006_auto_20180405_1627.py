# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-05 20:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0005_auto_20180405_1617'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='controle_despesas',
            unique_together=set([('data_viagem',)]),
        ),
    ]
