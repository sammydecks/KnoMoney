from django.contrib import admin
from .models import MyModel, TestTable


# Register your models here.
admin.site.register(MyModel)

# local DB table test
admin.site.register(TestTable)