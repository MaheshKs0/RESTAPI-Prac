from rest_framework import serializers
from .models import Trade

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'

    def validate_notional(self,value):
        if value<0:
            raise serializers.ValidationError("Notional value cannot be negative")
        return value

    def validate(self, attrs):
        if attrs.get('counterparty') is None or attrs.get('counterparty').strip() == "":
            raise serializers.ValidationError("counterparty cannot be null or empty")
        return attrs



