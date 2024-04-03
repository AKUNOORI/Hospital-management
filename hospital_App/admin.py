from django.contrib import admin
from .models import Patient, Doctors, Nurses, Profile, receptionist, Token, Invoice, Payment ,CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('groups', 'user_permissions')

    def groups_display(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    groups_display.short_description = 'Groups'

    def user_permissions_display(self, obj):
        return ", ".join([permission.name for permission in obj.user_permissions.all()])
    user_permissions_display.short_description = 'User Permissions'

    list_display = ('username', 'email', 'groups_display', 'user_permissions_display')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile", "medical_issue", "doj", "doe")

@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ("doctors_id","doctorName","start_time","end_time","availableTimeDate","endTimeDate","mobile","specialization")

@admin.register(Nurses)
class NursesAdmin(admin.ModelAdmin):
    list_display = ("nurses_id","nursesName","mobile","specialization", "availableTimeDate","endTimeDate")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user","phone_number","otp")

@admin.register(receptionist)
class receptionistAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile", "availableTimeDate", "endTimeDate")

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ("username", "age", "number","adhar", "gender", "disease", "address", "password")

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("patient", "invoice_number", "date_issued","due_date", "total_amount", "is_paid")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount_paid", "payment_date")

# admin.site.register(Doctors)