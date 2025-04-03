from django.db import models
from django.core.exceptions import ValidationError
from fundstates.models import AccountsInfo
from django.db import transaction
from django.db.models import Sum, F


# Create your models here.
class InvestmentSectors(models.Model):
    title = models.CharField(
        verbose_name="Short Title",
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Slug",
        max_length=100,
        unique=True,
    )
    investment_code = models.CharField(max_length=50, blank=False)
    investment_title = models.CharField(max_length=50, blank=False)
        
    class Meta:
        verbose_name = 'Investment Sector'
        verbose_name_plural = 'Investment Sectors'

    def __str__(self):
        return self.title
    

class InvestmentsInfo(models.Model):
    title = models.CharField(
        verbose_name="Short Title",
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Contribution Slug",
        max_length=100,
        unique=True,
    )
    descriptions = models.CharField(
        verbose_name="Give long descriptions",
        max_length=255,
    )
    invested_on = models.DateField(null=True)
    investments_codes = models.ForeignKey(
        InvestmentSectors, on_delete=models.CASCADE, related_name="investments")
    investments_funds = models.ForeignKey(
        AccountsInfo, on_delete=models.CASCADE, related_name="funds")
    
    invested_amount = models.DecimalField(
        verbose_name="amount",
        max_digits=12, decimal_places=2)
     
    class Meta:
        verbose_name = 'Investment Info'
        verbose_name_plural = 'Investments'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            investments_instance = self.investments_funds  
            
            if self.invested_amount  > investments_instance.current_balance:
                raise ValidationError(f"Fund Shortage! Your fund is {investments_instance.current_balance} but trying to invest {self.invested_amount }")

            investments_instance.current_balance = F('current_balance') - self.invested_amount
            investments_instance.save()

            super().save(*args, **kwargs)
