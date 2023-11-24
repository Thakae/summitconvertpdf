#FROM python:3.12
#
##
#WORKDIR /code
#
##
#COPY ./requirements.txt /code/requirements.txt
#
##
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#RUN pip install python-multipart
##
#COPY ./app /code/app
#
##
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install python-multipart
RUN pip install gunicorn

COPY . .

EXPOSE 3100

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:3100"]

