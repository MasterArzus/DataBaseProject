from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user

        # Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "hospital_management_app.admin_views":
                    pass
                elif modulename == "hospital_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("admin_home")

            elif user.user_type == "2":
                if modulename == "hospital_management_app.patient_views":
                    pass
                elif modulename == "hospital_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("patient_home")

            elif user.user_type == "3":
                if modulename == "hospital_management_app.doctor_views":
                    pass
                elif modulename == "hospital_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("doctor_home")

            else:
                return redirect("login")

        else:
            if request.path == reverse("login") or request.path == reverse("doLogin") or request.path == reverse(
                    "sign_up") or request.path == reverse("doRegister"):
                pass
            else:
                return redirect("login")
