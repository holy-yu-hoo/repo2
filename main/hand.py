import django
from django.db.models import Q, F, aggregates
from django.db.models.fields.json import KT

django.setup()
from app.models import Universe, Character, CharacterRelations
from app.utils import RelationType

total_bounty = Character.characters.annotate(bounty = KT('data__bounty')).aggregate(aggregates.Sum('bounty'), aggregates.Avg('bounty'))
print(total_bounty)
