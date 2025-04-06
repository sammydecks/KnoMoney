from django.contrib import admin
<<<<<<< HEAD
from .models import Referral


# Register your models here.
admin.site.register(Referral)
=======
from .models import MyModel, TestTable


# Register your models here.
admin.site.register(MyModel)

# local DB table test
admin.site.register(TestTable)
>>>>>>> 74054050e44e7d605d1bba8c8823d194525daad1
