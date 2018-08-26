from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from base.views import AdminRequiredView
from static_pages.forms import SendEmailToManagersForm, AddPageForm, EditPageForm
from static_pages.models import StaticPage
from users.models import User, UserType
from utils.mail import send_email
from django.utils.translation import ugettext as _

__all__ = ["SendEmailToManagersView", "PagesListView", "AddPageView", "PageDescriptionView", "EditPageView"]


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


class PagesListView(AdminRequiredView):
    def get(self, request):
        return render(request, "static_pages/statics_list.html", context={
            "pages": StaticPage.objects.all().order_by("-name").reverse()
        })


class AddPageView(View):

    def render_form(self, request, form):
        return render(request, 'static_pages/add_static_page.html', context={
            "form": form
        })

    def get(self, request):
        form = AddPageForm()
        return self.render_form(request, form)

    def post(self, request):
        form = AddPageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("New static page has been successfully added."))
            return HttpResponseRedirect(reverse("pages:add_new_page"))
        return self.render_form(request, form)


class PageDescriptionView(View):
    def get(self, request, page_name):
        static_page = get_object_or_404(StaticPage, short_name=page_name)
        return render(request, "static_pages/static_page_view.html", context={
            "page": static_page
        })


class EditPageView(AdminRequiredView):
    def render_form(self, request, form, page):
        return render(request, 'static_pages/edit_static_page.html', context={
            "form": form,
            "page": page
        })

    def get(self, request, page_name):
        static_page = get_object_or_404(StaticPage, short_name=page_name)
        form = EditPageForm(initial={
            'name': static_page.name,
            'is_visible': static_page.is_visible,
            'text': static_page.text
        })
        return self.render_form(request, form, static_page)

    def post(self, request, page_name):
        static_page = get_object_or_404(StaticPage, short_name=page_name)
        form = EditPageForm(request.POST, instance=static_page)
        if form.is_valid():
            form.update(static_page)
            messages.success(request, _("Static page has been updated."))
            return HttpResponseRedirect(reverse("pages:edit_page", args=(page_name,)))
        return self.render_form(request, form, static_page)
