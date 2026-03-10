from django.contrib import admin
from grooming_salon.loyalty_api.models import Voucher, Loyalty

# Register your models here.
#-----------------------------------------------------------------------------------------------------------------------
@admin.register(Loyalty)
class LoyaltyAdmin(admin.ModelAdmin):
    list_display = ('id','used_points','total_earned_points','current_points','remaining_until_reward','active_vouchers', 'created_at', 'user',)
    search_fields = ('id',)
    ordering = ('created_at',)

#-----------------------------------------------------------------------------------------------------------------------

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('id','code', 'is_used', 'created_at', 'user',)
    search_fields = ('code',)
    ordering = ('created_at',)

#-----------------------------------------------------------------------------------------------------------------------
