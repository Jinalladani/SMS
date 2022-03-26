from django.urls import path
from admin_panel import views

urlpatterns = [
    path('', views.AdminPanelDashboardView.as_view(), name='admin-panel-dashboard'),
    path('admin-login/', views.AdminLoginView.as_view(), name='admin-login'),

    path('admin-settings/', views.AdminSettingView.as_view(), name='admin-settings'),
    path('add-admin-settings/', views.AddAdminSettingView.as_view(), name='add-admin-settings'),
    path('update-admin-settings/<int:pk>', views.UpdateAdminSettingView.as_view(), name='update-admin-settings'),
    
    path('admin-societys/', views.AdminSocietysView.as_view(), name='admin-societys'),
    path('download-all-file/<int:pk>', views.DownloadAllFilesApiView.as_view(), name='download-all-file'),

]
