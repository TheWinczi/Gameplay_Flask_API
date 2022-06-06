FROM python:3.10

RUN mkdir /flask_app
RUN mkdir /flask_app/frontend
COPY ./frontend /flask_app/frontend

WORKDIR /flask_app/frontend

RUN pip install -r ./requirements.txt

ENV FLASK_APP=src
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=8080

ENTRYPOINT [ "python" ]
CMD [ "-m", "flask", "run", "--host", "0.0.0.0" ]
