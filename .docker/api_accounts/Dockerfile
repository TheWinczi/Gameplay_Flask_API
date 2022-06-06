FROM python:3.10

RUN mkdir /flask_app
RUN mkdir /flask_app/api_accounts
COPY ./api_accounts /flask_app/api_accounts

WORKDIR /flask_app/api_accounts

RUN pip install -r ./requirements.txt

ENV FLASK_APP=src
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=8083

ENTRYPOINT [ "python" ]
CMD [ "-m", "flask", "run", "--host", "0.0.0.0" ]
