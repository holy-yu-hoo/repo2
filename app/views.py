from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Universe, Character
import json


# XSS (Cross-Site Scripting)
# /search/?name=<script>alert('XSS')</script>
def search(request):
	search_query = request.GET.get('name', '')
	try:
		person = Character.characters.get(name__icontains = search_query)
		response = person
	except Character.DoesNotExist:
		response = None
	context = {'search_query': search_query, 'response': response}
	return render(request, 'search_view.html', context)


# SQL-injection
# /sql-injection/?name=' OR '1'='1
def search_2(request):
	character_name = request.GET.get('name', '')

	# вставляем напрямую в код запроса -> можно встроить что-то нехорошее
	query = f"SELECT * FROM app_character WHERE name LIKE '%{character_name}%' "

	with connection.cursor() as cursor:
		cursor.execute(query)
		results = cursor.fetchall()
		response = results if results else None
	print(results)
	context = {'search_query': character_name, 'response': response}
	return render(request, 'search_view.html', context)


# another SQL-injection
# /sql-filter/?universe_id=1 OR 1=1
def request_universe(request):
	universe_id = request.GET.get('universe_id', '1')

	# вставляем напрямую в код запроса -> можно встроить что-то нехорошее
	query = f"""
    SELECT * FROM app_character 
    WHERE id = {universe_id}
    """

	with connection.cursor() as cursor:
		cursor.execute(query)
		columns = [col[0] for col in cursor.description]
		results = [dict(zip(columns, row)) for row in cursor.fetchall()]

	return JsonResponse({'characters': results})


# CSRF (Cross-Site Request Forgery)
@csrf_exempt  # амернно отключим csrf
def csrf_vulnerable_form_view(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		author = request.POST.get('author')

		universe = Universe(title = title, author = author)
		universe.save()

		return HttpResponse(f'Вселенная "{title}" успешно создана!')

	form_html = """
    <html>
    <body>
        <h1>Создать новую вселенную</h1>
        <form method="POST">
            <!-- нету {% csrf_token %} -->
            Название вселенной: <input type="text" name="title"><br>
            Автор: <input type="text" name="author"><br>
            <input type="submit" value="Создать вселенную">
        </form>

        <hr>
        <h3>Существующие вселенные:</h3>
        <ul>
    """

	# существующие вселенные
	universes = Universe.universes.all()
	for universe in universes:
		form_html += f"<li>{universe.title} (автор: {universe.author})</li>"

	form_html += """
        </ul>
    </body>
    </html>
    """
	return HttpResponse(form_html)


# XSS
# /character/1/?message=<script>alert('XSS')</script>
def character_detail_xss(request, character_id):
	character = get_object_or_404(Character, id = character_id)

	# берем небезопасный ввод
	user_message = request.GET.get('message', '')

	# language=HTML
	response_html = f"""
    <html lang="en-us">
    <body>
        <h1>Персонаж: {character.name}</h1>
        <p>Вселенная: {character.universe.title}</p>
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
            <h3>Сообщение от пользователя:</h3>
            <div>
                {user_message}  <!-- XSS -->
            </div>
        </div>

        <form method="GET">
            Оставить сообщение: <input type="text" name="message">
            <input type="submit" value="Отправить">
        </form>
    </body>
    </html>
    """

	return HttpResponse(response_html)


def index(request):
	return render(request, 'index.html')
