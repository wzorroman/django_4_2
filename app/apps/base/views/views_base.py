import logging
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView


logger = logging.getLogger(__name__)


#  Create your views here.
def index(request):
    print(settings.BASE_DIR)
    return HttpResponse("Bienvenidos al app base")


class IndexView(TemplateView):
    template_name = 'index.html'

