from django.urls import path
from . import views
from .views import calculate_interest, calculate_whatif, calculate_savings_simple, get_interestrate, upload_referral, upload_calculation, upload_sharedemail

urlpatterns = [
    path("", views.home, name="home"),
    path("campus/", views.home, name="home"),
    path("music/", views.home, name="home"),
    path("online/", views.home, name="home"),
    path("calculate/", views.calculator, name="calculator"),
    path("faqs/", views.faq, name="faq"),

    path("calculate_interest", calculate_interest, name="calculate_interest"),
    path("calculate_whatif", calculate_whatif, name="calculate_whatif"),
    path("calculate_savings_simple", calculate_savings_simple, name="calculate_savings_simple"),
    path("get_interestrate", get_interestrate, name="get_interestrate"),

    # path("track-action/", track_action, name="track-action"),

    path("upload_referral/", upload_referral, name="upload_referral"),
    path("upload_sharedemail/", upload_sharedemail, name="upload_sharedemail"),
    path("upload_calculation/", upload_calculation, name="upload_calculation"),
]