FROM python:3.10.0-alpine

COPY resources/requirements.txt /project/
COPY resources/requirements-server.txt /project/

RUN pip install -r /project/requirements.txt
RUN pip install -r /project/requirements-server.txt

COPY src/ /project/src/
COPY setup.py /project/

RUN rm /project/src/teachertools/settings.py
RUN sh -c 'if [ ! -f /project/src/teachertools/settings.py ]; then echo "from teachertools.conf.docker_settings import *" > /project/src/teachertools/settings.py; fi'
RUN pip install -e /project

WORKDIR /project

# EXPOSE 8000
# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "teachertools.wsgi:application"]
CMD gunicorn teachertools.wsgi:application --bind 0.0.0.0:$PORT