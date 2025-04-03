from django.db import models

# Create your models here.
class AccountsInfo(models.Model):
    account_name = models.CharField(
        verbose_name="Account Info",
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Contribution Slug",
        max_length=100,  
        unique=True,
    )
    bank_account_name = models.CharField(
        verbose_name="Account Name",
        max_length=100,
        unique=True,
        null=True
    )
    account_no = models.CharField(
        verbose_name="Account no",
        max_length=100,
        unique=True,
    )
    bank_name = models.CharField(
        verbose_name="Bank Name",
        max_length=100,
        unique=True,
    )
    account_type = models.CharField(
        verbose_name="Account Type",
        max_length=30,
        unique=True,
        null=True
    )
    branch_name = models.CharField(
        verbose_name="branch_name",
        max_length=100,
        null=True,
        unique=True,
    ) 
    bank_Code = models.CharField(
        verbose_name="Bank Code",
        max_length=50,
        null=True,
        unique=True
    )
    routing_number = models.CharField(
        verbose_name="Bank Routing Number",
        max_length=55,
        unique=True,
        null=True
    ) 
    current_balance = models.DecimalField(
        verbose_name="account current balance",
        max_digits=12, decimal_places=2)
     
    class Meta:
        verbose_name = 'Uttoron Accounts Info'
        verbose_name_plural = 'Uttoron Accounts Info'

    def __str__(self):
        return self.account_name