from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator,MinLengthValidator
from django.utils.translation import gettext_lazy as _
# Create your models here.

class FiscalYear(models.Model):
    name = models.CharField(
        max_length=7,
        validators=[MinLengthValidator(7)]  
    )
    slug = models.SlugField(
        verbose_name="Fiscal Year",
        max_length=55,
        unique=True,
    )
         
    class Meta:
        verbose_name = 'Fiscal Year'
        verbose_name_plural = 'Fiscal Years'

    def __str__(self):
        return self.name

class Month(models.Model):
    name = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(3)]      
    )
  
    slug = models.SlugField(
        verbose_name="Month",
        max_length=20,
        unique=True,
    )
       
    class Meta:
        verbose_name = 'Month'
        verbose_name_plural = 'Months'

    def __str__(self):
        return self.name

