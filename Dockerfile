FROM python:3.8

WORKDIR /opt/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP /opt/api/src/app.py

# install postgres client
RUN apt update && \
    apt install postgresql-client -y && \
    rm -rf /var/cache/apt/archives

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile .
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pipenv install --system --skip-lock --dev --deploy

# setup a dev user
RUN useradd -ms /bin/bash dev 
USER dev

COPY . .

# Run Commands
EXPOSE 5000
ENTRYPOINT ["/opt/api/cmds/entrypoint.sh"]
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
