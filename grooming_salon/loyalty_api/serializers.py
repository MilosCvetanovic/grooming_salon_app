from rest_framework import serializers
from grooming_salon.loyalty_api.models import Loyalty, Voucher

# Create your serializers here.
#-----------------------------------------------------------------------------------------------------------------------
class LoyaltySerializer(serializers.ModelSerializer):
    current_points = serializers.ReadOnlyField()
    appointment_count = serializers.ReadOnlyField(source='total_earned_points')
    remaining_until_reward = serializers.ReadOnlyField()
    discount_available = serializers.SerializerMethodField()
    active_vouchers = serializers.SerializerMethodField()

    class Meta:
        model = Loyalty
        fields = ['id', 'current_points', 'appointment_count','remaining_until_reward', 'discount_available', 'active_vouchers', 'created_at']

    def get_discount_available(self, obj):
        if obj.current_points >= 5:
            return 'Dostupan vaučer za 20% popusta!'
        return f'Još {obj.remaining_until_reward} termina do popusta'

    def get_active_vouchers(self, obj):
        vouchers = Voucher.objects.filter(user=obj.user, is_used=False)
        return [v.code for v in vouchers]

#-----------------------------------------------------------------------------------------------------------------------
