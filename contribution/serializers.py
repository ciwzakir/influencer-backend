from rest_framework import serializers

from .models import CollectionsInfo

class CollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionsInfo
        fields = ['id','title','payment_image','received_from','receivable_month','amount',
                  'deposit_to','total_paid_by_user','total_deposit_by_all','current_payment_status','entry_date','references','payment_method','transaction_date']
        depth =  2

        