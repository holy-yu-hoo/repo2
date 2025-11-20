import django
from django.template.loader import get_template


django.setup()

template = get_template('file.djt')
value = [
	(1, 2),
	(3, 4),
	(5, 6),
	(7, 8),
]
print(template.render(context = {'value': value}))
