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


class IndexBlankView(TemplateView):
    template_name = 'backends/blank_base_demo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title_page = "Maestro | Client"
        main_title_content = "Clientes"
        main_subtitle_content = "Lista de clientes"
        subtitle_table = "Lista"

        context.update({
            'CLASS_MENU_MAESTROS': "menu-open",
            'CLASS_MENU_MAESTROS_SELECT': "active",
            'CLASS_MENU_0_CLIENT': "menu-open",
            'CLASS_MENU_0_CLIENT_SELECT': "active",
            'CLASS_MENU_1_CLIENT_ADD': "",
            'CLASS_MENU_1_CLIENT_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
        })
        return context


