FROM python
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install django


COPY . .
RUN #python manage.py collectstatic
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]