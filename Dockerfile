FROM python:3.11.4-alpine

ARG host=192.168.1.57
ENV HOST ${host}

ARG port=5432
ENV PORT ${port}

ARG bd=nova
ENV BD ${bd}

WORKDIR /code

COPY ./requeriments.txt /code/requeriments.txt

RUN pip install --no-cache-dir --upgrade -r /code/requeriments.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]