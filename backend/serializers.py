from rest_framework import serializers
from .models import QRTxnCallbackByEko, AepsTxnCallbackByEko, CMSTxnCallbackByEko

class QRTxnCallbackByEkoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRTxnCallbackByEko
        fields = '__all__'

class AepsTxnCallbackByEkoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AepsTxnCallbackByEko
        fields = '__all__'


class CMSTxnCallbackByEkoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMSTxnCallbackByEko
        fields = '__all__'
