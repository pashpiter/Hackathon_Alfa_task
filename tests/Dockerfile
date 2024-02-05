FROM python:3.10

ENV WORKDIR /tests
ENV USER tests
ENV PYTHONPATH $WORKDIR

WORKDIR $WORKDIR

RUN apt-get update && \
    apt-get install -y netcat-traditional

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry==1.4.2 && \
    poetry config virtualenvs.create false

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry install

COPY . .

RUN groupadd -r $USER && \
    useradd -d $WORKDIR -r -g $USER $USER && \
    chown $USER:$USER -R $WORKDIR && \
    chmod +x docker-entrypoint.sh

USER $USER

ENTRYPOINT ["./docker-entrypoint.sh"]