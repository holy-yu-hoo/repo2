from django import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import functools


# class CharacterForm(forms.ModelForm):
# 	class Meta:
# 		model = models.Character
# 		fields = ['name', 'universe_id']
#
# 		widgets = {
# 			'name': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'input name', 'autocomplete': 'off'}),
# 			'universe_id': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'input universe', 'autocomplete': 'off'}),
# 		}
# 		labels = {'name': 'name', 'universe': 'universe', }


class UniverseForm(forms.ModelForm):
	class Meta:
		model = models.Universe
		fields = ('title',)
		widgets = {
			'title': forms.TextInput(attrs = {'placeholder': 'input universe', 'autocomplete': 'off'}),
		}
		labels = {'title': 'title', }

class CharacterForm(forms.ModelForm):
	universe_title = forms.CharField(
		max_length = 100,
		widget = forms.TextInput(attrs = {
			'placeholder': 'input universe',
			'autocomplete': 'off',
			'class': 'form-field',
		}),
		label = 'Universe Title'
	)


	class Meta:
		model = models.Character
		fields = ('name',)
		widgets = {
			'name': forms.TextInput(attrs = {'placeholder': 'input character', 'autocomplete': 'off'}),
		}


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-field'

	def save(self, commit = True):
		universe_title = self.cleaned_data['universe title']
		name = self.cleaned_data['name']

		if models.Universe.universes.filter(title = universe_title).exists() and models.Character.characters.filter(name = name).exists():
			raise forms.ValidationError('A character already exists.')
		universe, created = models.Universe.universes.get_or_create(title = universe_title)
		character = models.Character(name = name, universe = universe)

		if commit: character.save()

		return character


class UserAuthorizationForm(forms.ModelForm):
	username = forms.CharField(required = True, widget = forms.TextInput(attrs = {
		'autocomplete': 'off',
	}))
	password = forms.CharField(required = True, widget = forms.PasswordInput)


	class Meta:
		model = User
		fields = ('username', 'password')


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print(self.fields)
		for field in self.fields:
			self.fields[field].widget.attrs['class'] = functools.class_attribute_formatter(['form-control'])

	def save(self, commit = True):
		user = super().save(commit)
		user.password = self.cleaned_data['password']
		if commit:
			user.save()
		return user()
