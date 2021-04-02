FROM python:3.9-slim

COPY . /app
WORKDIR /app

ENV PYTHON_BIN python3

RUN \
    echo "**** install pip packages ****" && \
    pip3 install -U pip setuptools wheel && \
    pip3 install -r requirements.txt && \
    echo "**** clean up ****" && \
    rm -rf \
        /root/.cache \
        /tmp/* \
        /var/lib/apt/lists/*

CMD ["/bin/sh", "run.sh", "--pass-errors", "--no-botenv"]