from django.contrib import admin
from .models import EmailList, LoanCalculation, IndividualLoan, SharedEmail, SimpleCalculation

# Register your models here.
admin.site.register(EmailList)
admin.site.register(SharedEmail)
admin.site.register(LoanCalculation)
admin.site.register(IndividualLoan)
admin.site.register(SimpleCalculation)
