from django.contrib import admin
from .models import Referral, TestTable, LoanCalculation, IndividualLoan

# Register your models here.
admin.site.register(Referral)
admin.site.register(LoanCalculation)
admin.site.register(IndividualLoan)

# local DB table test
admin.site.register(TestTable)
