import imp
from django import views
from django_datatables_view.base_datatable_view import BaseDatatableView
from admin_panel.models import SettingModel
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponse, Http404
import shutil
from django.contrib.auth import get_user_model
User = get_user_model()


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

class AdminSocietyListJSONView(BaseDatatableView):
    model = User
    columns = [
        'id',
        'society_name',
        'email',
        'phone',
        'city',
        'is_active'
    ]
    order_columns = [
        'id',
        'society_name',
        'email',
        'phone',
        'city',
        'is_active'
    ]

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(category__society_name=search))
        return qs

class ToggleSocietyIsActiveApiView(APIView):

    def post(self, request):
        society = User.objects.get(pk = request.POST.get('society_id'))
        society.is_active = not society.is_active
        society.save()
        return Response({"message": "Data Updated Successfully"})
class DeleteSocietyApiView(APIView):

    def delete(self, request, pk):
        # society = User.objects.get(pk = request.POST.get('society_id'))
        # society.delete()
        return Response({"message": "Data Deleted Successfully"})