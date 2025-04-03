from django.db import models
import datetime

class FinancialYear(models.Model):
    fiscal_year  = models.CharField(max_length=9, blank=True)
 
    class Meta:
        verbose_name = ("Financial Year")
        verbose_name_plural = ("Financial Years")

    def __str__(self):
        return self.fiscal_year

class SuperInfo(models.Model):
    name = models.CharField(max_length=100)
    rank = models.CharField(max_length=20)
    appointment = models.CharField(max_length=100)
 

    class Meta:
        verbose_name = ("Supervisor")
        verbose_name_plural = ("Supervisors")

    def __str__(self):
        return self.name

class AccountantsInfo(models.Model):
    name = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    appointment = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Accountants Info")
        verbose_name_plural = ("Accountants Info")

    def __str__(self):
        return self.name

class CounterSign(models.Model):
    name = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    appointment = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Counter Sign")
        verbose_name_plural = ("Counter Sign")

    def __str__(self):
        return self.name

class Additional(models.Model):
    title = models.CharField(max_length=70)
    expense_incurred = models.CharField(max_length=100)
    cheque_series = models.CharField(max_length=10)
    unit_name = models.CharField(max_length=50)
    
        
    class Meta:
        verbose_name = ("Additional")
        verbose_name_plural = ("Additional Info")
    
    def __str__(self):
        return self.title


class Signatures(models.Model):
    basic_info = models.CharField(max_length=50)
    supervisor_info = models.ForeignKey(SuperInfo, on_delete=models.CASCADE, verbose_name="Supervisor Info")
    accountant_info = models.ForeignKey(AccountantsInfo, on_delete=models.CASCADE, verbose_name="Accountant Info")
    counter_sign_info = models.ForeignKey(CounterSign, on_delete=models.CASCADE, verbose_name="Counter Sign")
    additional_info = models.ForeignKey(Additional, on_delete=models.CASCADE, verbose_name="Additional Info")
    with_effect_from = models.DateField(
        "Wef Date", default=datetime.date.today)
    
    
    class Meta:
        verbose_name = ("Signature")
        verbose_name_plural = ("Set Signatures")

    def __str__(self):
        return self.basic_info