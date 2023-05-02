FROM python:3.10

ENV PORT 8080
ENV PYTHONPATH=/code

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY data /code/data
COPY layout /code/layout
COPY rest /code/rest
COPY state /code/state

EXPOSE $PORT

CMD ["sh", "-c", "flask --app /code/rest/server run -p $PORT --host 0.0.0.0"]