from django.db import models


class RelationType(models.TextChoices):
	ENEMY = 'enemy', 'Враг'
	ALLY = 'ally', 'Союзник'
	FRIEND = 'friend', 'Друг'
	RIVAL = 'rival', 'Соперник'
	MENTOR = 'mentor', 'Наставник'
	STUDENT = 'student', 'Ученик'
