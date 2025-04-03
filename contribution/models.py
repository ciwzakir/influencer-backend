from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.text import slugify
from basics.models import FiscalYear, Month
from fundstates.models import AccountsInfo
from userprofile.models import User
from django.db.models import Sum, F
import os
from django.utils.translation import gettext_lazy as _

class MonthlyContributionInfo(models.Model):
    name = models.CharField(
        verbose_name="Contribution Title",
        help_text="Contribution Amount",
        max_length=55,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Contribution Slug",
        max_length=55,
        unique=True,
    )
    fiscal_year = models.ForeignKey(
        FiscalYear, 
        verbose_name="Fiscal Year",
        on_delete=models.RESTRICT,
        related_name="fiscal")
    contribution_month = models.ForeignKey(
        Month,
        verbose_name="Contribution Month",
        on_delete=models.RESTRICT, 
        related_name="month")
    contribution_amount = models.DecimalField(
        verbose_name="Contribution Amount",
        max_digits=12, decimal_places=2)
   
    
    class Meta:
        verbose_name = 'Payable Amount'
        verbose_name_plural = 'Payable Amount'

    def __str__(self):
        return self.name

class CollectionsInfo(models.Model):
    DUE = 'due'
    VERIFICATION_PENDING = 'verification'
    PAID = 'paid'

    PAYMENT_STATUS_CHOICES = [
        (DUE, 'Dues'),
        (VERIFICATION_PENDING, 'Verification Pending'),
        (PAID, 'Paid'),
    ]
    title = models.CharField(
        verbose_name="Short Description",
        help_text="About ..",
        max_length=55,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Received Slug",
        max_length=55,
        unique=True,
    )
    received_from = models.ForeignKey(
        User, 
        verbose_name="Received From",
        on_delete=models.CASCADE, default=1)
    
    deposit_to = models.ForeignKey(
        AccountsInfo, 
        verbose_name="Deposited Account",
        on_delete=models.CASCADE, default=1)
    
    entry_date = models.DateField(null=True)

    receivable_month = models.ForeignKey(
        MonthlyContributionInfo, 
        verbose_name="For the month",
        on_delete=models.CASCADE, related_name="receivable")
    references = models.CharField(max_length=100)
    transaction_date = models.DateField(null=True)
    payment_method = models.CharField(
        verbose_name="Bank/Bkash/Card/Other",
        max_length=50,
        null=True
    )
    amount = models.DecimalField(
        verbose_name="Paid Amount",
        max_digits=12, decimal_places=2)
    payment_image = models.ImageField(
        verbose_name="Picture or screenshot",
        upload_to='images/payment',
        null=True)
    current_payment_status = models.CharField(
        max_length=12,
        choices=PAYMENT_STATUS_CHOICES,
        default=DUE,
    )

       
    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        with transaction.atomic():
            receive_from_instance = self.received_from
            receivable_month_instance = self.receivable_month
            receivable_month_instance_id = self.receivable_month.id  
            deposit_instance = self.deposit_to
           
            # existing_payment = CollectionsInfo.objects.filter(
            #     received_from=receive_from_instance,
            #     receivable_month=receivable_month_instance_id,  
            #     current_payment_status=current_payment_status_instance,
            # ).exists()

            existing_payment = CollectionsInfo.objects.filter(
            received_from=receive_from_instance,
            receivable_month=receivable_month_instance_id,
            current_payment_status="paid"  
            ).exists()


            if existing_payment:
                raise ValidationError(
                    f"You have already paid for {self.receivable_month.contribution_month.name}."
                    f"Fiscal Year: {self.receivable_month.fiscal_year.name}"
                )
            # Validate payment amount
            expected_amount = receive_from_instance.membershipinfo.share * receivable_month_instance.contribution_amount
            
            if self.amount != expected_amount:
                raise ValidationError(f"You are supposed to deposit {expected_amount}, but you are trying to deposit {self.amount}.")
            
            if self.current_payment_status == "paid":
                deposit_instance.current_balance = F('current_balance') + self.amount
                deposit_instance.save()          

            super().save(*args, **kwargs)

    def total_deposit_by_all(self):
        """
        Calculate the total amount deposited by all users with payment status as 'paid'.
        """
        return CollectionsInfo.objects.filter(
        current_payment_status="paid"  
        ).aggregate(
        all_paid=Sum('amount')
        )['all_paid'] or 0.00

    def total_paid_by_user(self):
        """
        Calculate the total amount paid by this user across all months with payment status as 'paid'.
        """
        return CollectionsInfo.objects.filter(
            received_from=self.received_from,
            current_payment_status="paid"  # Filter by 'paid' status
        ).aggregate(
            total_paid=Sum('amount')
        )['total_paid'] or 0.00

    @staticmethod
    def total_paid_by_specific_user(user_profile):
        """
        Calculate the total amount paid by a specific user with payment status as 'paid'.
        """
        return CollectionsInfo.objects.filter(
            received_from=user_profile,
            current_payment_status="paid"  # Filter by 'paid' status
        ).aggregate(
            total_paid=Sum('amount')
        )['total_paid'] or 0.00

    @staticmethod
    def total_paid_for_specific_month_and_user(month, user_profile):
        """
        Calculate the total amount paid by a specific user for a specific month with payment status as 'paid'.
        """
        return CollectionsInfo.objects.filter(
            receivable_month__contribution_month=month,
            received_from=user_profile,
            current_payment_status="paid"  # Filter by 'paid' status
        ).aggregate(
            total_paid=Sum('amount')
        )['total_paid'] or 0.00
