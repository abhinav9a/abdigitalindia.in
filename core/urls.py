from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('terms-and-conditions', views.termsAndConditions, name='termsAndConditions'),
    path('privacy-policy', views.privacyPolicy, name='privacyPolicy'),
    path('refund-cancellation', views.refundCancellation, name='refundCancellation'),
]
