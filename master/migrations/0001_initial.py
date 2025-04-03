# Generated by Django 5.1 on 2025-03-05 12:46

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import master.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('primary', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required and Unique', max_length=255, unique=True, verbose_name='Code Full Name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Budget Code Slug')),
                ('seven_digit_code', models.IntegerField(validators=[master.models.validate_seven_digits, django.core.validators.MinValueValidator(1000000), django.core.validators.MaxValueValidator(9999999)])),
                ('is_general', models.BooleanField(default=True)),
                ('heading', models.CharField(max_length=255)),
                ('economic_segment', models.CharField(choices=[('PAY', 'Pay and Allowance'), ('REPAIR', 'Repair and Maintenance'), ('ASSETS', 'Assets Collection')], default='REPAIR', max_length=255)),
                ('lp_auth', models.CharField(max_length=255)),
                ('voucher_head', models.CharField(max_length=3)),
                ('total_alloted_amounts', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total_refund_amounts', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('progress_of_allotments', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Progressive Allotment')),
                ('progress_of_expenses', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Progressive Expense')),
                ('current_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Unspent Balance')),
            ],
            options={
                'verbose_name': 'Budget Code',
                'verbose_name_plural': 'Budget Codes',
            },
        ),
        migrations.CreateModel(
            name='Consumerunit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('slug', models.SlugField(max_length=25, unique=True)),
                ('parent_office', models.CharField(db_index=True, max_length=50)),
            ],
            options={
                'verbose_name': 'Consumer Unit Name',
                'verbose_name_plural': 'Consumer Unit Names',
            },
        ),
        migrations.CreateModel(
            name='Procurementprovider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('tin_no', models.CharField(max_length=13)),
                ('vat_no', models.CharField(max_length=13)),
                ('regpage_no', models.CharField(max_length=13, verbose_name='Register Page No')),
                ('is_registered', models.BooleanField(default=True)),
                ('reg_date', models.DateField()),
            ],
            options={
                'verbose_name': 'Procurement Provider Name',
                'verbose_name_plural': 'Procurement Provider Names',
            },
        ),
        migrations.CreateModel(
            name='Allotment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required', max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('alloted_on', models.DateField(verbose_name='Allotment Date')),
                ('alloted_auth', models.CharField(default='23.03.2600.039.51.001.21.000/ A', max_length=70, verbose_name='Vide Ltr Reference')),
                ('alloted_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('allotment_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allotments', to='master.category', verbose_name='Budget Codes')),
                ('alloted_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.consumerunit', verbose_name='For Which Office')),
            ],
            options={
                'verbose_name': 'Allotment',
                'verbose_name_plural': 'Allotment',
                'ordering': ('allotment_code',),
            },
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required', max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_cheque', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=False)),
                ('taxrate', models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Income TAX Rate')),
                ('complex_tax', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Complex TAX Amount')),
                ('vatrate', models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='VAT Rate')),
                ('complex_vat', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name=' Complex VAT Amount')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_allotments_codewise', models.DecimalField(decimal_places=2, default=0.0, help_text='Automated. Do not insert any value here', max_digits=12, verbose_name='Progress of Allotments')),
                ('total_expense_codewise', models.DecimalField(decimal_places=2, default=0.0, editable=False, help_text='Automated. Do not insert any value here', max_digits=12, verbose_name='Progress of Expense')),
                ('total_exp', models.DecimalField(decimal_places=2, default=0.0, editable=False, help_text='Automated. Do not insert any value here', max_digits=12, verbose_name='Total of Single Bills')),
                ('total_tds', models.DecimalField(decimal_places=2, default=0.0, editable=False, help_text='Automated. Do not insert any value here', max_digits=10, verbose_name='Tax deducted at Source')),
                ('total_vds', models.DecimalField(decimal_places=2, default=0.0, editable=False, help_text='Automated. Do not insert any value here', max_digits=10, verbose_name='VAT deducted at Source')),
                ('total_paid', models.DecimalField(decimal_places=2, default=0.0, editable=False, help_text='Automated. Do not insert any value here', max_digits=12, verbose_name='Payable Amount of the Bill')),
                ('consumer_unit', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='master.consumerunit', verbose_name='Consumer Office Name')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenditures', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('expenditure_code', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='alt_exp', to='master.category', verbose_name='Budget Codes')),
                ('fiscal_year', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='fy', to='primary.financialyear')),
                ('on_change_charge', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='charge', to='primary.signatures')),
                ('item_supplier', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='master.procurementprovider', verbose_name='Select Your Supplier')),
            ],
            options={
                'verbose_name': 'Expenditure',
                'verbose_name_plural': 'Expenditures',
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required', max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('refund_on', models.DateField(verbose_name='Refunded Date')),
                ('refund_auth', models.CharField(default='23.03.2600.039.51.001.21.000/ A', max_length=70, verbose_name='Vide Ltr Reference')),
                ('refund_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('refund_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refund_allotments', to='master.category', verbose_name='Budget Codes')),
                ('refund_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.consumerunit', verbose_name='For Which Office')),
            ],
            options={
                'verbose_name': 'Refund Allotment',
                'verbose_name_plural': 'Refund Allotments',
                'ordering': ('refund_code',),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=30)),
                ('invoice_date', models.DateField()),
                ('lp_no', models.CharField(max_length=6)),
                ('receivevoucher_no', models.CharField(max_length=8)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('invoices', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='master.expenditure')),
            ],
            options={
                'verbose_name': 'Invoice Detail',
                'verbose_name_plural': 'Invoice Details',
                'unique_together': {('invoices', 'invoice_no')},
            },
        ),
    ]
