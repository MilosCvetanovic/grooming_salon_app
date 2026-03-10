from rest_framework import serializers
from grooming_salon.loyalty_api.models import Loyalty


# Create your serializers here.
#-----------------------------------------------------------------------------------------------------------------------
class LoyaltySerializer(serializers.ModelSerializer):
    appointment_count = serializers.ReadOnlyField()
    discount_available = serializers.SerializerMethodField()

    class Meta:
        model = Loyalty
        fields = ['id', 'points', 'appointment_count', 'discount_available', 'created_at']

    def get_discount_available(self, obj):
        if obj.points >= 5:
            return '20% POPUSTA'
        return 'Još uvek nemate popust'

#-----------------------------------------------------------------------------------------------------------------------
