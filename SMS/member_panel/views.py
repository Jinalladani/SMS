from email import contentmanager
import imp
from django.shortcuts import redirect, render
from django.template import context
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.conf import settings
import requests
from random import randint
import phonenumbers
from django.contrib import messages

from accounting.models import SocietyMemberDetailsModel
from member_panel.forms import MemberLoginForm
from member_panel.models import OtpModel

from member_panel.mixins import MemberLoginRequired, RedirectIfLoggedIn

# Create your views here.

class MemberDashboard(MemberLoginRequired, TemplateView):

    def get(self, request):
        context = {}
        return render(request, "member-panel/member-dashboard.html", context)

class MemberLoginView(RedirectIfLoggedIn, View):

    def get(self, request):
        context = {}
        form = MemberLoginForm()
        context['form'] = form
        return render(request, "member-panel/member-login.html", context)

    def post(self, request):
        context = {}
        form = MemberLoginForm(request.POST)

        if form.is_valid():
            mobile_number = form.cleaned_data["mobile_number"]
            Member = SocietyMemberDetailsModel.objects.filter(Q(primary_contact_no= mobile_number) | Q(secondary_contact_no= mobile_number) | Q(whatsapp_contact_no= mobile_number))
            try:
                if Member:
                    otp = randint(100000, 999999)
                    requests.get(settings.SMSURL.format(phone_no= mobile_number, otp= otp))
                    obj, created = OtpModel.objects.update_or_create(mobile_number= mobile_number, defaults={"otp": otp})
                    request.session['mobile_number'] = mobile_number.raw_input
                    return redirect("member-otp-verification")
                else:
                    form.add_error(None, "Mobile Number is not registered.")
                    context['form'] = form
                    return render(request, "member-panel/member-login.html", context)
            except Exception as e:
                print(e)
        else:
            context['form'] = form
            return render(request, "member-panel/member-login.html", context)

class MemberOtpVerification(RedirectIfLoggedIn, View):

    def get(self, request):
        context = {}
        return render(request, "member-panel/member-otp-verification.html", context)

    def post(self, request):
        context = {}
        otp = request.POST.get("otp")
        mobile_number = phonenumbers.parse(request.session['mobile_number'], None)

        stored_otp = OtpModel.objects.filter(mobile_number= mobile_number).first().otp

        if int(stored_otp) == int(otp):
            request.session["is_verified"] = True
            return redirect('member-dashboard')
        else:
            request.session["is_verified"] = False
            messages.add_message(request, messages.INFO, "OTP is not valid.")
            return render(request, "member-panel/member-otp-verification.html", context)