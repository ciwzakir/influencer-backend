from rest_framework import serializers

from .models import Category, Expenditure, Transaction, Allotment, Refund
from primary.models import Signatures, SuperInfo, Additional, AccountantsInfo, CounterSign,FinancialYear




class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = ('__all__')

class SuperInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperInfo
        fields = ('name', 'rank', 'appointment')

class AdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional
        fields = ('title','expense_incurred', 'cheque_series', 'unit_name')

class AccountantsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountantsInfo
        fields = ('name', 'rank', 'appointment')

class CounterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterSign
        fields = ('name', 'rank', 'appointment')

class PrimarySettingsSerializer(serializers.ModelSerializer):
    supervisor_info = SuperInfoSerializer(read_only=True)
    additional_info = AdditionalSerializer(read_only=True)
    accountant_info = AccountantsInfoSerializer(read_only=True)
    counter_sign_info = CounterInfoSerializer(read_only=True)

    class Meta:
        model = Signatures
        fields = ('basic_info','supervisor_info', 'additional_info', 'accountant_info', 'counter_sign_info','with_effect_from')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'invoice_date', 'amount', 'invoice_no','lp_no', 'receivevoucher_no')


class ExpenditureSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)
    on_change_charge = PrimarySettingsSerializer()

    class Meta:
        model = Expenditure
        fields = ('id','fiscal_year','updated_at','slug','expenditure_code',
                  'consumer_unit', 'item_supplier', 'created_by','title',
                  'transactions','get_prog_alts','get_totals','taxrate','get_income_tax',
                  'get_value_added_tax','get_paid_amount', 'get_children_length','is_cheque','vatrate','is_published','on_change_charge', 'bills_status'

                 )
        depth =  1



class AllotmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allotment
        fields = ('__all__')
        depth =  1

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ('__all__')
        depth =  1



class CodeWiseSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Expenditure
        fields = ('__all__')
        depth =  1

class CategoryWiseSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)

    class Meta:
        model = Category
        fields = ('transactions',)


        fields = ('transactions',)

class SupplierWiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenditure
        fields = ('__all__')
        depth =  1



class ErrorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenditure
        fields = ('title','get_tds_errors','get_vds_errors','get_expense_errors','get_cross_check_errors')


