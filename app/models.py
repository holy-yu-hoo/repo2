from django.db import models
from django.db.models import functions
from app.utils import RelationType


# Create your models here.
class Universe(models.Model):
	title = models.CharField('universe title',
		unique = True,
		max_length = 200,
		blank = True)
	author = models.CharField(max_length = 200,
		default = None,
		blank = True,
		null = True)
	universes = models.Manager()

	def __str__(self):
		return f'{self.title}'

	def __repr__(self):
		return f'<Universe {self.title}>'


	class Meta:
		verbose_name = 'universe'
		verbose_name_plural = 'universes'
		constraints = [
			models.UniqueConstraint(fields = ['title', 'author'],
				name = 'universe_author_unique'),
		]


class CharacterQuerySet(models.QuerySet):

	def get_queryset(self):
		return self.annotate(relations_num = models.aggregates.Count('relations'))

	def total_bounties(self):
		return self.aggregate(
			total_bounties = models.Sum(
				models.functions.Coalesce(functions.Cast('data__bounty', models.IntegerField()), 0),
			))['total_bounties']


class Character(models.Model):
	name = models.CharField('character name',
		unique = True,
		max_length = 200,
		blank = True)
	universe = models.ForeignKey(
		Universe,
		on_delete = models.CASCADE,
		db_column = 'universe',
		verbose_name = 'universe',
		related_name = 'characters',
		related_query_name = 'character',
		help_text = 'Universe of this character',
	)
	relations = models.ManyToManyField(
		'self',
		through = 'CharacterRelations',
		through_fields = ('character_a', 'character_b'),
		related_name = 'related_characters',
		related_query_name = 'related_character',

		symmetrical = False,
	)

	data = models.JSONField(blank = True,
		null = True,
		default = dict)

	objects = models.Manager()
	characters = models.Manager.from_queryset(CharacterQuerySet)()

	def __str__(self):
		return f'{self.name}'

	def __repr__(self):
		return f'<Character {self.name} from {self.universe}>'


	@property
	def canonic(self):
		return self.canon

	@canonic.setter
	def canonic(self,
		value: bool):
		if value not in (True, False):
			raise ValueError('Canonic must be True or False')
		self.canon = value

	def set_universe_by_tile(self,
		universe_tile: str):
		try:
			universe = Universe.universes.get(title__iexact = universe_tile)
		except Universe.DoesNotExist:
			universe = Universe(title = universe_tile.title())
		self.universe = universe

	def save(self,
		*args,
		**kwargs):
		if self.universe and self.universe.pk is None:  # if yet not existing universe
			self.universe.save()
		super().save(*args,
			**kwargs)


	class Meta:
		constraints = (
			models.UniqueConstraint(fields = ['name', 'universe'],
				name = 'character_universe_unique'),
		)
		indexes = (
			models.Index(fields = ['name'],
				name = 'character_name_idx'),
		)
		verbose_name = 'character'
		verbose_name_plural = 'characters'
		ordering = ['name']


class CharacterRelations(models.Model):
	"""character A's relationship to character B"""
	character_a = models.ForeignKey(
		Character,
		on_delete = models.CASCADE,
		db_column = 'character_a',
		related_name = 'rel_character_a',

	)

	character_b = models.ForeignKey(
		Character,
		on_delete = models.CASCADE,
		db_column = 'character_b',
		related_name = 'rel_character_b',
	)

	relation_type = models.CharField(
		max_length = 20,
		choices = RelationType.choices,
		default = RelationType.ENEMY,
	)

	def __str__(self):
		return f'Relation of {self.character_a} to {self.character_b} is {self.relation_type}'

	__repr__ = __str__


	class Meta:
		db_table = 'app_character_relations'
