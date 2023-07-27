FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 80

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --default-timeout=2000 -r requirements.txt

COPY . /app/

RUN python manage.py makemigrations --no-input
RUN python manage.py migrate --no-input

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@admin.com
ENV DJANGO_SUPERUSER_PASSWORD=admin123

RUN python manage.py createsuperuser --no-input

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]