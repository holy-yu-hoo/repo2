from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.forms.models import model_to_dict
from . import forms
from . import models
from . import tools
from django.db import connection
from django.template.response import TemplateResponse


def user_registration_view(request):
	context = dict()
	if request.method == 'POST':
		form = forms.UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.user
			request.session['user'] = model_to_dict(user)
			request.session.set_expiry(0)
			return redirect(reverse('main:user_home', args = (user.login,)))
		else:
			context['form'] = form
	else:
		context['form'] = forms.UserRegistrationForm()
	return render(request, 'main/user_registration.html', context = context)


def user_login_view(request):
	context = dict()
	if request.method == 'POST':
		form = forms.UserLoginForm(request.POST)
		if form.is_valid():
			user = form.user
			request.session['user'] = model_to_dict(user)
			request.session.set_expiry(0)
			return redirect(reverse('main:user_home', args = (user.login,)))
		else:
			context['form'] = form
	else:
		context['form'] = forms.UserLoginForm()
	return render(request, 'main/user_registration.html', context = context)


def user_logout_view(request):
	request.session.flush()
	return redirect('main:index')


def index(request):
	return render(request, "main/general_page.html")


@tools.PermissionsResolver('login')
def user_home_page_view(request, login):
	context = dict()
	user = models.User.objects.get(login = login)
	context['user'] = user
	return render(request, "main/user_home_page.html", context = context)


@tools.PermissionsResolver('owner')
def user_home_page_edit_view(request, login):
	context = dict()
	user = models.User.objects.get(login = login)
	if request.method == "POST":
		userprofile = user.profile
		for field_name, field_value in request.POST.items():
			field_name = field_name.split('-')[-1]
			setattr(userprofile, field_name, field_value)
		userprofile.save()
		messages.success(request, "i am saved")
		return redirect('main:user_home_edit', login = login)
	context['user'] = user
	return render(request, "main/user_home_edit_page.html", context = context)


def search_view(request):
	context = dict()
	if request.method == 'POST':
		search_request = request.POST.get('search_request', '')
	else:
		search_request = request.GET.get('search_request', '')
	# search_result = (
	# 	models.User.objects.filter(login__contains = search_request) |
	# 	models.User.objects.filter(profile__name__contains = search_request) |
	# 	models.User.objects.filter(profile__surname__contains = search_request)
	# )

	with connection.cursor() as cursor:
		cursor.execute(
			f"""select * from main_user
				join main_userprofile on (main_user.id = main_userprofile.user_id)
			where login like '%{search_request}%' or name like '%{search_request}%' or surname like '%{search_request}%'""",
		)
		keys = ("id", "login", "password", "user_id", "name", "surname", "about")
		search_result = [dict(zip(keys, i)) for i in cursor.fetchall()]
		print(search_result)
	context['search_request'] = search_request
	context['search_result'] = search_result
	return render(request, "main/search_page.html", context = context)
