FROM python:3.10

RUN mkdir /flask_app
RUN mkdir /flask_app/api_players
COPY ./api_players /flask_app/api_players

WORKDIR /flask_app/api_players

RUN pip install -r ./requirements.txt

ENV FLASK_APP=src
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=8081

ENTRYPOINT [ "python" ]
CMD [ "-m", "flask", "run", "--host", "0.0.0.0" ]
