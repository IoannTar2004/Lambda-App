FROM python:3.12-slim as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ARG ENVFILE=.env.example

ENV PATH=/root/.local/bin:$PATH
ENV ENV_FILE=$ENVFILE

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y docker.io
RUN rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8003

CMD ["sh", "-c", "rm -rf /usr/code_archives/* && python -u app/execution_service_main.py"]
