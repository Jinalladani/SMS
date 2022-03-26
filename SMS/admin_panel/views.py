import imp
from django.shortcuts import render
from django.views import View
from django.contrib.auth import views as auth_views
from django.views.generic.edit import FormView
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth import (
    REDIRECT_FIELD_NAME,
    get_user_model,
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.http import (
    url_has_allowed_host_and_scheme,
    urlsafe_base64_decode,
)
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, QueryDict
from django.conf import settings
from django.shortcuts import resolve_url
from django.contrib.sites.shortcuts import get_current_site

from admin_panel.forms import AdminAuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from django.views.generic import CreateView, UpdateView
from admin_panel.models import SettingModel
from django.http import HttpResponse, Http404

from django.contrib.auth import get_user_model
User = get_user_model()


class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}


class AdminLoginView(SuccessURLAllowedHostsMixin, FormView):
    """
    Display the login form and handle the login action.
    """

    form_class = AdminAuthenticationForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "admin-panel/admin-login.html"
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url("admin-panel-dashboard")

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name, "")
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                self.redirect_field_name: self.get_redirect_url(),
                "site": current_site,
                "site_name": current_site.name,
                **(self.extra_context or {}),
            }
        )
        return context

class AdminPanelDashboardView(View):
    def get(self, request):
        context = {}
        admins = User.objects.filter(is_superuser=False)
        all_list = admins.count()
        active = admins.filter(is_active=True).count()
        deactive = admins.filter(is_active=False).count()
        context['all_list'] = all_list
        context['active'] = active
        context['deactive'] = deactive
        return render(request, "admin-panel/admin-dashboard.html", context)


class AdminSettingView(View):

    def get(self, request):
        context = {}
        return render(request, "admin-panel/admin-settings.html", context)

class AddAdminSettingView(CreateView):
    model = SettingModel
    fields = ['key', 'value']
    template_name = 'admin-panel/settings-add.html'
    success_url = '/admin-panel/admin-settings/'

class UpdateAdminSettingView(UpdateView):
    model = SettingModel
    fields = ['key', 'value']
    template_name = 'admin-panel/settings-update.html'
    success_url = '/admin-panel/admin-settings/'

class AdminSocietysView(View):

    def get(self, request):
        context = {}
        return render(request, "admin-panel/admin-societys.html", context)


class DownloadAllFilesApiView(View):

    def get(self, request, pk):
        try:
            # zip_path = shutil.make_archive(settings.MEDIA_ROOT + '\\zip\\' + "ledger_file_"+User.objects.get(pk=pk).society_name, "zip", settings.MEDIA_ROOT + '\\' + "ledger_file_"+User.objects.get(pk=pk).society_name)
            zip_file = open("D:\Videos\work\Bonrix\Phase 2\SMS\SMS\media\zip\ledger_file_Shreeji Charan Society.zip", 'r', encoding="utf8")
            response = HttpResponse(zip_file, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename="%s"' % 'D:\Videos\work\Bonrix\Phase 2\SMS\SMS\media\zip\ledger_file_Shreeji Charan Society.zip'
            return response

        except Exception as e:
            raise Http404