import imp
from django import views
from django_datatables_view.base_datatable_view import BaseDatatableView
from admin_panel.models import SettingModel
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

class AdminSettingsListJSONView(BaseDatatableView):
    model = SettingModel
    columns = [
        'id',
        'key',
        'value'
    ]
    order_columns = [
        'id',
        'key',
        'value'
    ]

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(category__key=search))
        return qs

class AdminSettingsDeleteView(APIView):
    authentication_classes = [SessionAuthentication]

    def delete(self, request, pk):
        object = SettingModel.objects.get(pk=pk)
        object.delete()
        return Response({"message": "Data Deleted Successfully"})