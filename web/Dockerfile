FROM python:3.9
ENV PYTHONUNBUFFERED=1
# WORKDIR /botcode
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
# Collect static files
# RUN python manage.py collectstatic --noinput