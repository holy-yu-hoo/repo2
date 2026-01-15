from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
# from django.contrib.auth import login,logout
from django.contrib.auth import authenticate, login, logout
from . import forms
from . import models
import json


@permission_required('app.add_character', raise_exception = True)
def index(request):
	return render(request, 'app/index.html')


def logout_view(request):
	logout(request)
	return redirect(reverse('app:login'))


class ReqView(LoginRequiredMixin, TemplateView):
	template_name = 'app/index.html'
	raise_exception = True
	permission_denied_message = "if you can't access this page, tell your mom about it"

# permission_required = ('app.add_character',)
