FROM registry1.dso.mil/ironbank/opensource/python/python38:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-warn-script-location

COPY . /app

ENV PORT=8080

USER root

RUN python -m pip install pyOpenSSL --no-warn-script-location && \
    python tls_generator.py && \
    python -m pip uninstall -y pyOpenSSL 

USER python3

CMD ["python", "main.py"]