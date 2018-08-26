from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import ugettext as _

from base.views import AdminRequiredView, LoginRequiredView
from users.forms import RegisterForm, LoginForm, ChangePasswordForm, SendEmailToUsersForm, AddUserForm, ProfileForm
from users.models import User, UserType
from utils.mail import send_email

__all__ = ["RegisterView", "RegisterWithLinkView", "LoginView", "LogoutView", "ChangePasswordView",
           "SendEmailToUsersView", "AddUserView", "UsersListView", "ProfileView"]


class NotAuthenticatedView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next = request.GET.get("next", request.POST.get("next", reverse("index")))
            return HttpResponseRedirect(next)
        else:
            return super().dispatch(request, *args, **kwargs)


class RegisterView(NotAuthenticatedView):

    def render_form(self, request, form):
        return render(request, 'users/register.html', context={
            "form": form
        })

    def get(self, request):
        form = RegisterForm()
        return self.render_form(request, form)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("You have been successfully registered."))
            return HttpResponseRedirect(reverse("users:login"))
        return self.render_form(request, form)


class RegisterWithLinkView(RegisterView):
    def get(self, request):
        form = RegisterForm(initial={'email': 'peyman.jabarzade@gmail.com'})
        form.fields['email'].__setattr__('disabled', True)
        return self.render_form(request, form)


class LoginView(NotAuthenticatedView):
    def render_form(self, request, form):
        return render(request, 'users/login.html', context={
            "form": form
        })

    def get(self, request):
        form = LoginForm(request)
        return self.render_form(request, form)

    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            messages.success(request, _("You have been logged in successfully."))
            next = request.GET.get("next", request.POST.get("next", reverse("index")))
            return HttpResponseRedirect(next)
        return self.render_form(request, form)


class LogoutView(LoginRequiredView):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        messages.success(request, _("You have been logged out successfully."))
        return HttpResponseRedirect(reverse("index"))


class ChangePasswordView(LoginRequiredView):
    def render_form(self, request, form):
        return render(request, 'users/change-password.html', context={
            "form": form
        })

    def get(self, request):
        form = ChangePasswordForm(request.user)
        return self.render_form(request, form)

    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your password was successfully updated.'))
            next = request.GET.get("next", request.POST.get("next", reverse("index")))
            return HttpResponseRedirect(next)
        return self.render_form(request, form)


class SendEmailToUsersView(AdminRequiredView):
    def render_form(self, request, form):
        return render(request, 'send-email.html', context={
            "form": form
        })

    def get(self, request):
        form = SendEmailToUsersForm()
        return self.render_form(request, form)

    def post(self, request):
        form = SendEmailToUsersForm(request.POST)
        if form.is_valid():
            active_users = User.objects.filter(is_active=True)

            if send_email(request.POST['subject'], request.POST['text'], active_users):
                messages.success(request, _('Your email has been send successfully.'))
            else:
                messages.warning(request, _('Your email has not been send.'))
            next = request.GET.get("next", request.POST.get("next", reverse("index")))
            return HttpResponseRedirect(next)
        return self.render_form(request, form)


class AddUserView(AdminRequiredView):
    def render_form(self, request, form):
        return render(request, 'users/add-user.html', context={
            "form": form
        })

    def get(self, request):
        form = AddUserForm()
        return self.render_form(request, form)

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("User has been successfully added."))
            return HttpResponseRedirect(reverse("users:add_user"))
        return self.render_form(request, form)


class UsersListView(AdminRequiredView):
    def get(self, request):
        return render(request, "users/users_list.html", context={
            "users": User.objects.filter(is_superuser=False).order_by("-email").reverse()
        })


class ProfileView(AdminRequiredView):
    def render_form(self, request, form, user):
        return render(request, 'users/profile.html', context={
            "form": form,
            "user": user
        })

    def get(self, request, link):
        user = User.objects.filter(link=link)[0]
        form = ProfileForm(initial={
            'name': user.name,
            'is_active': user.is_active
        })
        return self.render_form(request, form, user)

    def post(self, request, link):
        user = User.objects.filter(link=link)[0]
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.update(user)
            messages.success(request, _("User has been updated."))
            return HttpResponseRedirect(reverse("users:profile", args=(link,)))
        return self.render_form(request, form, user)
