from django.urls import path
from . import views
from .views import calculate_interest

urlpatterns = [
    path("", views.home, name="home"),
    path("campus/", views.home, name="home"),
    path("music/", views.home, name="home"),
    path("online/", views.home, name="home"),
    path("calculate/", views.calculator, name="calculator"),
    path("faqs/", views.faq, name="faq"),

    path("calculate_interest", calculate_interest, name="calculate_interest"),
]