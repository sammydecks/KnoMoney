from django.contrib import admin
from .models import Referral, LoanCalculation, IndividualLoan, SharedEmail

# Register your models here.
admin.site.register(Referral)
admin.site.register(SharedEmail)
admin.site.register(LoanCalculation)
admin.site.register(IndividualLoan)
