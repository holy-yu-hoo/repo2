Необходимо установить python и sqlite

После скачивания и установки:
Заходим терминалом в папку проекта и
pip install -r requirements.txt
Для установки необходимых модулей python

И если все установилось
python manage.py runserver 8080

перейти в браузере по http://localhost:8080/

Примеры уязвимостей
Переход по http://127.0.0.1:8080/main/search/?search_request="<script>setTimeout(() => {alert(("xss-attack\ncsrf-token: ").concat(document.getElementsByName("csrfmiddlewaretoken")[0].value));}, 1000);</script>"

Ввод в поле Search

' or true --
Приведет к sql-injection (и удалит базу данных)

Дополнительная информация
Уже существующие пользователи:

login | password

user1 123
user2 123
user3 123
user4 123
user5 123
Логин и пароль админа (по адресу http://localhost:8080/admin/) admin и 123 соответственно