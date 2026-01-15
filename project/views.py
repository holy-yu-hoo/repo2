from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView


class ErrorBaseView(TemplateView):
	error_code = None
	error_message = ""
	template_name = 'project/error_base.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["error_code"] = self.error_code
		context['error_message'] = self.error_message
		return context


class Error400View(ErrorBaseView): error_code = 400; error_message = 'Bad Request';


class Error403View(ErrorBaseView): error_code = 403; error_message = 'Forbidden';


class Error404View(ErrorBaseView): error_code = 404; error_message = 'Page Not Found';


class Error500View(ErrorBaseView): error_code = 500; error_message = 'Internal Server Error';


def index(request):
	raise PermissionDenied
