from django.shortcuts import redirect


class MemberLoginRequired:

    def dispatch(self, request, *args, **kwargs):
        try:
            verified = request.session["is_verified"]
            if verified:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("member-login")
        except KeyError as e:
            return redirect("member-login")

class RedirectIfLoggedIn:

    def dispatch(self, request, *args, **kwargs):
        try:
            verified = request.session["is_verified"]
            if verified:
                return redirect("member-dashboard")
            else:
                return super().dispatch(request, *args, **kwargs)
        except KeyError as e:
            return redirect("member-login")