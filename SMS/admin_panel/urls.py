from django.urls import path
from admin_panel import views

urlpatterns = [
    path('', views.AdminPanelDashboardView.as_view(), name='admin-panel-dashboard'),
    path('admin-login/', views.AdminLoginView.as_view(), name='admin-login'),
]
