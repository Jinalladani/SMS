from django.urls import path
from member_panel import views

urlpatterns = [
    path('', views.MemberDashboard.as_view(), name='member-dashboard'),
    path('member-login/', views.MemberLoginView.as_view(), name='member-login'),
    path('member-otp-verification/', views.MemberOtpVerification.as_view(), name='member-otp-verification'),
]
