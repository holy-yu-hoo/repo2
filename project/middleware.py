from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpRequest


class YMiddleware:

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request: HttpRequest):
		val = request.session.get('visiting', 0)
		request.session['visiting'] = val + 1
		response = self.get_response(request)
		return response
