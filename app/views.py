from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.conf import settings
from importlib import import_module

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore()


class IndexView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({'data': 'i have data'})
		return context

	def get(self, request, *args, **kwargs):
		response = super().get(request, *args, **kwargs)
		response.cookies['key'] = 'i am cookie'
		return response
