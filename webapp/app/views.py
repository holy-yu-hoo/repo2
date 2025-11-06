from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from . import forms
from django.contrib import messages
from . import models


def index(request):
	if request.method == 'POST':
		form = forms.CharacterForm(request.POST)
		if form.is_valid():
			try:
				form.save()
			except Exception as e:
				print(e)
			else:
				print('Valid form')

		else:
			print("Not a valid form")
		return redirect('/', request)
	return render(request, 'app/index.html', {'form': forms.CharacterForm()})


def authorization(request):
	if request.method == 'POST':
		form = forms.UserAuthorizationForm(request.POST)
		if form.is_valid():
			try:
				form.save()
			except Exception as e:
				print(e)
			else:
				print('Valid form')
		return redirect('/authorization/', request)
	return render(request, 'app/authorization.html', {'form': forms.UserAuthorizationForm()})

# def check_character_existing(request):
# 	name = request.GET.get('name', '')
# 	universe = request.GET.get('universe', '')
#
# 	# print('check character existence')
#
# 	if name and universe:
# 		# print(name, universe)
# 		exists = True  # exists = models.Character.characters.filter(name__iexact = name, universe__iexact = universe).exists()
#
# 		return HttpResponse('True' if exists else 'False')
#
# 	return HttpResponse('False')
