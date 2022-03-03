from multiprocessing.spawn import import_main_path
from django.urls import path
from admin_panel.api import views


urlpatterns = [
    path('list-admin-settings/', views.AdminSettingsListJSONView.as_view(), name='list-admin-settings'),
    path('admin-settings/delete/<int:pk>/', views.AdminSettingsDeleteView.as_view(), name='delete-admin-settings'),
]