from django.contrib import admin
from .models import UserAccount, ContactForm
from django.utils.translation import gettext_lazy as _

# Register your models here.

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username','userType','email','is_active','kycStatus')

    fieldsets = (
        (None, {"fields": ('username','password', 'userType', 'shopName', 'pancard_no')}),
        (_('Personal info'),{'fields':('profile_img', 'first_name', 'last_name', 'email', 'mobile', 'dob', 'address')}),
        (_('Bank info'),{'fields':('acc_name', 'acc_type', 'acc_no', 'ifsc', 'payment_mode')}),
        (_('Permissions'),{'fields':('unique_sequence','platform_id', 'eko_user_code', 'userManager', 'kycStatus', 'is_active' , 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'message')

    

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(ContactForm, ContactFormAdmin)