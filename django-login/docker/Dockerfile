FROM python:3.7

ENV PYTHONUNBUFFERED=1

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code


# runs the production server
CMD python manage.py runserver 0.0.0.0:8080