from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.db import transaction
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from primary.models import FinancialYear, Signatures
from django.utils import timezone



def validate_seven_digits(value):
    if len(str(value)) != 7:
        raise ValidationError("Value must be a 7-digit number.")

class Category(models.Model):

    SEGMENT_CHOICES = [
    ("PAY", "Pay and Allowance"),
    ("REPAIR", "Repair and Maintenance"),
    ("ASSETS", "Assets Collection"),
]
    name = models.CharField(
        verbose_name="Code Full Name",
        help_text="Required and Unique",
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Budget Code Slug",
        max_length=255,
        unique=True,
    )
    seven_digit_code = models.IntegerField(
        validators=[validate_seven_digits, MinValueValidator(1000000), MaxValueValidator(9999999)],
        blank=False )


    is_general = models.BooleanField(default=True)
    heading = models.CharField(max_length=255, blank=False)
    economic_segment = models.CharField(max_length=255,  choices=SEGMENT_CHOICES,
        default='REPAIR',)
    lp_auth = models.CharField(max_length=255, blank=False)
    voucher_head = models.CharField(max_length=3, blank=False)
    total_alloted_amounts = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00,)
    total_refund_amounts = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00,)
    progress_of_allotments = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Progressive Allotment")
    progress_of_expenses = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Progressive Expense")
    current_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, verbose_name="Unspent Balance")

    def get_allotment_totals(self):
        sub_total = 0
        sub_total = Allotment.objects.filter(allotment_code=self).aggregate(
            total=Sum('alloted_amount'))['total'] or 0.00
        return Decimal(sub_total)

    def get_refunds_totals(self):
        refunds_total = 0
        refunds_total = Refund.objects.filter(refund_code=self).aggregate(
            total=Sum('refund_amount'))['total'] or 0.00
        return Decimal(refunds_total)

    def get_current_prog_of_allotment(self):
        current_allotment__prg = 0
        current_allotment__prg = self.get_allotment_totals() - self.get_refunds_totals()
        return Decimal(current_allotment__prg)

    def get_current_prog_of_expense(self):
        sub_expenses = 0
        sub_expenses = Expenditure.objects.filter(expenditure_code=self).aggregate(
            total=Sum('total_exp'))['total'] or 0.00
        return Decimal(sub_expenses)

    def your_current_balance(self):
        current_balance = 0
        current_balance = self.get_current_prog_of_allotment() - self.get_current_prog_of_expense()
        return Decimal(current_balance)

    def save(self, *args,**kwargs):

        super(Category, self).save(*args, **kwargs)

        self.total_alloted_amounts = self.get_allotment_totals()
        self.total_refund_amounts = self.get_refunds_totals()
        self.progress_of_allotments = self.get_current_prog_of_allotment()
        self.progress_of_expenses = self.get_current_prog_of_expense()
        self.current_balance = self.your_current_balance()
        ttl_allotted_prog = self.get_current_prog_of_allotment()
        ttl_refunded_amount  = self.get_refunds_totals()
        refunds_err_msg = "Total Refund amount must be less than tatal Proggress of Allotments for respective Budget Code.Check."
        refunds_err_msg = "Your Expense must be less than allotment."
        the_current_balance = self.your_current_balance()

        if ttl_refunded_amount> ttl_allotted_prog:
            raise ValidationError(f" {refunds_err_msg}  || Check  {self.name}  ")
        elif the_current_balance <0 :
            raise ValidationError(f" {refunds_err_msg}  || Check  {self.name}  ")
        # self.current_balance.save()
        return super(Category,self).save(*args,**kwargs)


    class Meta:
        verbose_name = 'Budget Code'
        verbose_name_plural = 'Budget Codes'

    def __str__(self):
        return self.name


class Consumerunit(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=25, unique=True)
    parent_office = models.CharField(max_length=50, db_index=True)

    class Meta:
        verbose_name = "Consumer Unit Name"
        verbose_name_plural = "Consumer Unit Names"

    def __str__(self):
        return self.name


class Procurementprovider(models.Model):
    name = models.CharField(
        verbose_name="Name",
        help_text="Required",
        max_length=255,
        blank=False,
    )
    slug = models.SlugField(max_length=255, unique=True)
    address = models.CharField(max_length=255,)
    tin_no = models.CharField(max_length=13, blank=False,)
    vat_no = models.CharField(max_length=13, blank=False,)
    regpage_no = models.CharField(max_length=13, blank=False, verbose_name="Register Page No",)
    is_registered = models.BooleanField(default=True)
    reg_date = models.DateField()

    class Meta:
        verbose_name = "Procurement Provider Name"
        verbose_name_plural = "Procurement Provider Names"

    def __str__(self):
        return self.name

    def get_ser_no(self):
        len_of_sup = 0
        len_of_sup = len(Expenditure.objects.filter(item_supplier=self))
        return Decimal(len_of_sup)


class Allotment(models.Model):
    allotment_code = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="allotments", verbose_name="Budget Codes")
    alloted_unit = models.ForeignKey(
        Consumerunit, on_delete=models.CASCADE, verbose_name="For Which Office")
    title = models.CharField(
        verbose_name="title",
        help_text="Required",
        max_length=255)

    slug = models.SlugField(max_length=255, unique=True)
    alloted_on = models.DateField(verbose_name="Allotment Date")
    alloted_auth = models.CharField(
        max_length=70, default="23.03.2600.039.51.001.21.000/ A", verbose_name="Vide Ltr Reference")
    alloted_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00,)

    class Meta:
        verbose_name = 'Allotment'
        verbose_name_plural = 'Allotment'
        ordering = ('allotment_code',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

            category_instance = self.allotment_code

            if category_instance.your_current_balance() <0 :
                raise ValidationError("Refund amount is more than Balance?")

            current_prog_of_allotment = category_instance.get_current_prog_of_allotment()
            current_prog_of_expense = category_instance.get_current_prog_of_expense()
            your_current_balance = category_instance.your_current_balance()

            total_alloted_amounts = Allotment.objects.filter(allotment_code=self.allotment_code).aggregate(
                total_alloted_amounts=models.Sum('alloted_amount')
            )['total_alloted_amounts'] or 0.00

            Category.objects.filter(id=self.allotment_code.id).update(
                total_alloted_amounts=total_alloted_amounts,
                progress_of_allotments=current_prog_of_allotment,
                progress_of_expenses=current_prog_of_expense,
                current_balance=your_current_balance
            )


class Refund(models.Model):
    refund_code = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="refund_allotments", verbose_name="Budget Codes")
    refund_unit = models.ForeignKey(Consumerunit, on_delete=models.CASCADE, verbose_name="For Which Office")
    title = models.CharField(
        verbose_name="title",
        help_text="Required",
        max_length=255)

    slug = models.SlugField(max_length=255, unique=True)
    refund_on = models.DateField(verbose_name="Refunded Date")
    refund_auth = models.CharField(
        max_length=70, default="23.03.2600.039.51.001.21.000/ A", verbose_name="Vide Ltr Reference")
    refund_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00,)
    approved = models.BooleanField("Approved", default=False,)

    class Meta:
        verbose_name = 'Refund Allotment'
        verbose_name_plural = 'Refund Allotments'
        ordering = ('refund_code',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

            category_instance = self.refund_code

            if category_instance.get_refunds_totals() > category_instance.get_allotment_totals():
                raise ValidationError("Refund amount is more than Allotment?")
            elif category_instance.your_current_balance() <0 :
                raise ValidationError("Refund amount is more than Balance?")


            current_prog_of_allotment = category_instance.get_current_prog_of_allotment()
            current_prog_of_expense = category_instance.get_current_prog_of_expense()
            your_current_balance = category_instance.your_current_balance()

            total_refund_amounts = Refund.objects.filter(refund_code=self.refund_code).aggregate(
                total_refund_amounts=models.Sum('refund_amount')
            )['total_refund_amounts'] or 0.00

            Category.objects.filter(id=self.refund_code.id).update(
                total_refund_amounts=total_refund_amounts,
                progress_of_allotments=current_prog_of_allotment,
                progress_of_expenses=current_prog_of_expense,
                current_balance=your_current_balance
            )


class Expenditure(models.Model):

    STATUS_CHOICES = [
    ("PAID", "Already paid"),
    ("AWAITING", "Awaiting for payment"),
    ("PENDING", "Pending"),
    ("SENT_BACK", "Sent Back for correction"),
    ]

    title = models.CharField(
        verbose_name="title",
        help_text="Required",
        max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    fiscal_year = models.ForeignKey(
        FinancialYear, on_delete=models.RESTRICT, related_name="fy")
    on_change_charge = models.ForeignKey(
        Signatures, on_delete=models.RESTRICT, related_name="charge")
    expenditure_code = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="alt_exp", verbose_name="Budget Codes")
    consumer_unit = models.ForeignKey(
        Consumerunit, on_delete=models.RESTRICT, verbose_name="Consumer Office Name")
    item_supplier = models.ForeignKey(
        Procurementprovider, on_delete=models.RESTRICT, verbose_name="Select Your Supplier")
    is_cheque = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    bills_status = models.CharField(
        choices=STATUS_CHOICES,
        default='PENDING',
        max_length=20
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenditures",
        verbose_name="Created By",
    )
    taxrate = models.DecimalField(
        blank=False, max_digits=4, decimal_places=2, verbose_name="Income TAX Rate", default=0)
    complex_tax = models.DecimalField(
        blank=False, max_digits=8, decimal_places=2, verbose_name="Complex TAX Amount", default=0)
    vatrate = models.DecimalField(
        blank=False, max_digits=4, decimal_places=2, verbose_name="VAT Rate", default=0)
    complex_vat = models.DecimalField(
        blank=False, max_digits=8, decimal_places=2, verbose_name=" Complex VAT Amount", default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    total_allotments_codewise = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name=
        "Progress of Allotments",  help_text="Automated. Do not insert any value here",)
    total_expense_codewise = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name=
        "Progress of Expense",  help_text="Automated. Do not insert any value here", editable=False)
    total_exp = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name=
        "Total of Single Bills",  help_text="Automated. Do not insert any value here", editable=False)
    total_tds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=
        "Tax deducted at Source",  help_text="Automated. Do not insert any value here",editable=False)
    total_vds = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=
        "VAT deducted at Source",  help_text="Automated. Do not insert any value here",editable=False)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name=
        "Payable Amount of the Bill",  help_text="Automated. Do not insert any value here",editable=False)

    class Meta:
        verbose_name = 'Expenditure'
        verbose_name_plural = 'Expenditures'

    def clean(self):
        if not self.on_change_charge or not self.fiscal_year:
            raise ValidationError("Both fiscal_year and on_change_charge must be set.")

    def __str__(self):
        return (f"{self.title} & tk {self.total_exp}")

    def get_prog_alts(self):
        net_total = self.expenditure_code.get_current_prog_of_allotment()
        return net_total

    def get_totals(self):
        totals = 0
        net_total = 0
        for x in Transaction.objects.filter(invoices=self):
            totals += x.amount
            net_total = Decimal(totals)
        return net_total

    def get_income_tax(self):
        tax = 0
        tax_rate = self.taxrate
        tax_amount = self.complex_tax
        if tax_rate == 0 and tax_amount == 0:
            return Decimal(tax)
        elif tax_rate < 0 or tax_amount < 0:
            raise ValidationError("Insert positive Number")
        elif tax_rate > 0 and tax_amount > 0:
            raise ValidationError("Insert Rate or IT Amount")
        elif tax_rate == "" or tax_amount =="":
            raise ValidationError("Insert Rate or IT Amount Should not be blank")
        elif tax_rate > 0 and tax_amount == 0:
            income_tax = self.get_totals() * tax_rate / 100
            return Decimal(income_tax)
        elif tax_rate == 0 and tax_amount > 0:
            return Decimal(tax_amount)
        else:
            return Decimal(tax)

    def get_value_added_tax(self):
        vat = 0
        vat_rate = self.vatrate
        vat_amount = self.complex_vat
        if vat_rate == 0 and vat_amount == 0:
            return Decimal(vat)
        elif vat_rate < 0 or vat_amount < 0:
            return Decimal(vat)
        elif vat_rate < 0 or vat_amount < 0:
            raise ValidationError("Insert Positive Value")
        elif vat_rate > 0 and vat_amount > 0:
            raise ValidationError("Insert Rate or VAT Amount")
        elif vat_rate == "" or vat_amount =="":
            raise ValidationError("Insert Rate or VAT Amount Should not be blank")
        elif vat_rate > 0 and vat_amount == 0:
            vat_is = self.get_totals() * vat_rate / 100
            return Decimal(vat_is)
        elif vat_rate == 0 and vat_amount > 0:
            return Decimal(vat_amount)
        else:
            return Decimal(vat)

    def get_tds_errors(self):
        get_errors_msg = 'No error in TAX'
        negative_tds_msg = f" Negative Value as TAX is not accepted. Correction is required for {self.taxrate} or  {self.complex_tax}"
        tds_conflict_msg = f"Insert tolat TAX amount or tax rate. Do not insert both. Insert {self.taxrate} or  {self.complex_tax}"

        tax_rate = self.taxrate
        tax_amount = self.complex_tax

        if tax_rate < 0 or tax_amount < 0:
            raise ValidationError(negative_tds_msg)
        elif tax_rate > 0 and tax_amount > 0:
            raise ValidationError(tds_conflict_msg)
        else:
            return get_errors_msg

    def get_vds_errors(self):
        get_succress_msg = 'No error in VAT'
        negative_msg = f" Negative Value as VAT is not accepted. Insert positive value of {self.vatrate} or  {self.complex_vat}"
        tds_conflict_msg = f"Insert tolat VAT amount or vat rate. Do not insert both. Insert {self.vatrate} or  {self.complex_vat}"
        vat_rate = self.vatrate
        vat_amount = self.complex_vat

        if vat_rate < 0 or vat_amount < 0:
            raise ValidationError(negative_msg)
        elif vat_rate > 0 and vat_amount > 0:
            raise ValidationError(tds_conflict_msg)
        else:
            return get_succress_msg

    def get_expense_errors(self):
        expense_err_msg = "Total Expense amount must be less than tatal Allotments for each Budget Code. Please add Allotment or expense it after getting allotment"
        get_valid_exp_msg = 'Expense Successful'
        a = self.expenditure_code.get_current_prog_of_expense()
        b = self.expenditure_code.get_current_prog_of_allotment()
        if a > b:
            raise ValidationError(
                f"{expense_err_msg} .You are trying to expense {a} from {b}. Please check {self.expenditure_code}")
        return get_valid_exp_msg

    def get_paid_amount(self):
        net_payable = 0
        ttl_amount = self.get_totals()
        sum_of_it_vat = self.get_income_tax() + self.get_value_added_tax()
        net_payable = ttl_amount - sum_of_it_vat
        return Decimal(net_payable)

    def get_cross_check_errors(self):

        recheck_msg = f" The sum of IT, VAT and paid amount is greater than gross subtotal of bills.  IT {self.get_income_tax()} + VAT  {self.get_value_added_tax()} +  Paid {self.get_paid_amount()}  =  Gross {self.get_totals()} ??? Please check {self.expenditure_code}"

        it_vat_paid_amount = self.get_income_tax() + self.get_value_added_tax() + \
            self.get_paid_amount()

        if it_vat_paid_amount == self.get_totals():
            return ("Success ")
        else:
            raise ValidationError(
                f" Sorry !  ||  Please Check your Expense  ||  {self.title}  ||   {recheck_msg}")

    def get_children(self):
        return Transaction.objects.filter(invoices=self)

    def get_children_length(self):
        get_len = len(Transaction.objects.filter(invoices=self))
        return Decimal(get_len)

    def get_serial_no(self):
        purchase_times = 0
        purchase_times = self.item_supplier.get_ser_no()
        return Decimal(purchase_times)

    def get_page_no(self):
        get_page_no = 0
        get_page_no = Decimal(self.item_supplier.regpage_no)
        get_length = Decimal(self.get_serial_no())
        if get_length > 1:
            return get_page_no + 1
        elif get_length > 2:
            return get_page_no + 2
        elif get_length > 3:
            return get_page_no + 3
        return Decimal(get_page_no)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

            category_instance = self.expenditure_code

            # if self.get_totals() > category_instance.your_current_balance() :
            #     raise ValidationError(f"Exp {self.get_totals()} amount is more than Balance {category_instance.your_current_balance()}")

            current_prog_of_expense = category_instance.get_current_prog_of_expense()
            your_current_balance = category_instance.your_current_balance()

            Category.objects.filter(id=self.expenditure_code.id).update(
                progress_of_expenses=current_prog_of_expense,
                current_balance=your_current_balance
            )


            self.total_allotments_codewise = self.expenditure_code.get_current_prog_of_allotment()
            self.total_expense_codewise = self.expenditure_code.get_current_prog_of_expense()
            self.total_exp = self.get_totals()
            self.total_tds = self.get_income_tax()
            self.total_vds = self.get_value_added_tax()
            self.total_paid = self.get_paid_amount()
            total_current_balance = self.expenditure_code.your_current_balance()
            exp_of_this_bill = self.get_totals()

            if self.get_paid_amount() < 0:
                raise ValidationError(
                    f"Please Check your Expense.(IT) {self.get_income_tax()} + (VAT) {self.get_value_added_tax()} + (Paid) {self.get_paid_amount()} is not eqaul to  gross amount {self.get_totals()}")

            elif self.total_allotments_codewise < self.total_expense_codewise:
                raise ValidationError(
                    f"Insufficient Balance. Balance is balane is {total_current_balance} and you are trying to expense {exp_of_this_bill} ")
            return super().save(*args, **kwargs)


class Transaction(models.Model):
    invoices = models.ForeignKey(
        Expenditure, on_delete=models.CASCADE, related_name="transactions")
    invoice_no = models.CharField(max_length=30)
    invoice_date = models.DateField()
    lp_no = models.CharField(max_length=6)
    receivevoucher_no = models.CharField(max_length=8)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Invoice Detail"
        verbose_name_plural = "Invoice Details"
        unique_together = ('invoices', 'invoice_no')
