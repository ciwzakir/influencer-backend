# Generated by Django 5.1 on 2024-09-29 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fundstates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyContributionInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Contribution Amount', max_length=55, unique=True, verbose_name='Contribution Title')),
                ('slug', models.SlugField(max_length=55, unique=True, verbose_name='Contribution Slug')),
                ('contribution_amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Contribution Amount')),
            ],
            options={
                'verbose_name': 'Payable Amount',
                'verbose_name_plural': 'Payable Amount',
            },
        ),
        migrations.CreateModel(
            name='CollectionsInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='About ..', max_length=55, unique=True, verbose_name='Short Description')),
                ('slug', models.SlugField(max_length=55, unique=True, verbose_name='Received Slug')),
                ('entry_date', models.DateField(null=True)),
                ('references', models.CharField(max_length=100)),
                ('transaction_date', models.DateField()),
                ('payment_method', models.CharField(max_length=50, verbose_name='Bank/Bkash/Card/Other')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Paid Amount')),
                ('payment_image', models.ImageField(upload_to='images/payment', verbose_name='Picture or screenshot')),
                ('current_payment_status', models.CharField(choices=[('due', 'Super User'), ('verification', 'Admin'), ('paid', 'paid')], default='due', max_length=12)),
                ('deposit_to', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fundstates.accountsinfo', verbose_name='Deposited Account')),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
        ),
    ]
