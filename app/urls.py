from django.urls import path
from . import views
from .views import calculate_interest, calculate_whatif, calculate_savings_simple

urlpatterns = [
    path("", views.home, name="home"),
    path("campus/", views.home, name="home"),
    path("music/", views.home, name="home"),
    path("online/", views.home, name="home"),
    path("calculate/", views.calculator, name="calculator"),
    path("faqs/", views.faq, name="faq"),

    path("calculate_interest", calculate_interest, name="calculate_interest"),
    path("calculate_whatif", calculate_whatif, name="calculate_whatif"),
    path("calculate_savings_simple", calculate_savings_simple, name="calculate_savings_simple")
]