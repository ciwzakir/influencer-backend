# Generated by Django 5.1 on 2025-03-05 12:46

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountantsInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rank', models.CharField(max_length=50)),
                ('appointment', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Accountants Info',
                'verbose_name_plural': 'Accountants Info',
            },
        ),
        migrations.CreateModel(
            name='Additional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('expense_incurred', models.CharField(max_length=100)),
                ('cheque_series', models.CharField(max_length=10)),
                ('unit_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Additional',
                'verbose_name_plural': 'Additional Info',
            },
        ),
        migrations.CreateModel(
            name='CounterSign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rank', models.CharField(max_length=50)),
                ('appointment', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Counter Sign',
                'verbose_name_plural': 'Counter Sign',
            },
        ),
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiscal_year', models.CharField(blank=True, max_length=9)),
            ],
            options={
                'verbose_name': 'Financial Year',
                'verbose_name_plural': 'Financial Years',
            },
        ),
        migrations.CreateModel(
            name='SuperInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rank', models.CharField(max_length=20)),
                ('appointment', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Supervisor',
                'verbose_name_plural': 'Supervisors',
            },
        ),
        migrations.CreateModel(
            name='Signatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_info', models.CharField(max_length=50)),
                ('with_effect_from', models.DateField(default=datetime.date.today, verbose_name='Wef Date')),
                ('accountant_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='primary.accountantsinfo', verbose_name='Accountant Info')),
                ('additional_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='primary.additional', verbose_name='Additional Info')),
                ('counter_sign_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='primary.countersign', verbose_name='Counter Sign')),
                ('supervisor_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='primary.superinfo', verbose_name='Supervisor Info')),
            ],
            options={
                'verbose_name': 'Signature',
                'verbose_name_plural': 'Set Signatures',
            },
        ),
    ]
