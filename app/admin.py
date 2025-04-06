from django.contrib import admin
from .models import Referral, TestTable

# Register your models here.
admin.site.register(Referral)

# local DB table test
admin.site.register(TestTable)
