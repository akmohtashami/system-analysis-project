from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from static_pages.forms import SendEmailToManagersForm
from users.models import User, UserType
from utils.mail import send_email
from django.utils.translation import ugettext as _

__all__ = ["SendEmailToManagersView"]


class SendEmailToManagersView(View):
    def render_form(self, request, form):
        return render(request, 'send-email.html', context={
            "form": form
        })

    def get(self, request):
        form = SendEmailToManagersForm()
        return self.render_form(request, form)

    def post(self, request):
        form = SendEmailToManagersForm(request.POST)
        if form.is_valid():
            active_admins = User.objects.filter(type=UserType.Admin).filter(is_active=True)

            if (send_email(_('Feedback'),
                           render_to_string('static_pages/email.html', context={"name": request.POST['name'],
                                                                         "email": request.POST['email'],
                                                                         "text": request.POST['text']}),
                           active_admins)):
                messages.success(request, _('Your email has been send successfully.'))
            else:
                messages.warning(request, _('Your email has not been send.'))
            next = request.GET.get("next", request.POST.get("next", reverse("index")))
            return HttpResponseRedirect(next)
        return self.render_form(request, form)
