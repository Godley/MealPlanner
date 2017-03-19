FROM python:3.5-alpine
COPY . ./app
WORKDIR ./app
EXPOSE 8000
RUN pip3 install -r requirements.txt
CMD python3 manage.py runserver