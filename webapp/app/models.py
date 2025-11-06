from django.db import models
from django.contrib import admin


class Universe(models.Model):
	title = models.CharField(max_length = 100, unique = True)
	autor = models.CharField(max_length = 100, blank = True, null = True)
	universes = models.Manager()


	class Meta:
		verbose_name = 'Universe'
		verbose_name_plural = 'Universes'


	def __str__(self):
		return f'{self.title}'

class Character(models.Model):
	name = models.CharField(max_length = 100)
	universe = models.ForeignKey(Universe, on_delete = models.CASCADE, related_name = 'characters')
	canonic = models.BooleanField(default = False)

	characters = models.Manager()


	class Meta:
		verbose_name = 'Character'
		verbose_name_plural = 'Characters'
		unique_together = ('name', 'universe')


	def __str__(self):
		return f'{self.name}'
