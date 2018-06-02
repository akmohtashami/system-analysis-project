from django.shortcuts import render
from django.views import View


class RequestTypeView(View):
    def get(self, request):
        return render(request, 'request-type-form.html')
