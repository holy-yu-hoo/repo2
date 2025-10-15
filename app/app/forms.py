from django import forms

from . import models


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
			'title': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'input name', 'autocomplete': 'off'}),
		}
		labels = {'title': 'title', }

class CharacterForm(forms.ModelForm):
	universe_title = forms.CharField(max_length = 100, label = 'Universe')


	class Meta:
		model = models.Character
		fields = ('name',)
		widgets = {}


	def save(self, commit = True):
		universe_title = self.cleaned_data['universe_title']
		name = self.cleaned_data['name']

		if models.Universe.universes.filter(title = universe_title).exists() and models.Character.characters.filter(name = name).exists():
			raise forms.ValidationError('A character already exists.')
		universe, created = models.Universe.universes.get_or_create(title = universe_title)
		character = models.Character(name = name, universe = universe)

		print(models.Character.universe)
		print(models.Character.name)

		if commit: character.save()

		return character
