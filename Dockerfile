# --- builder (Install Python Libraries)
FROM python:3.10 AS builder

WORKDIR /app
COPY ./requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock

# --- base (Setup for Application)
FROM python:3.10-slim AS base

RUN apt-get update && apt-get install -y \
  openssl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN groupadd -r app \
  && useradd --no-log-init -m -g app app \
  && mkdir /app \
  && chown app /app

USER app
WORKDIR /app
ENV PYTHONPATH /app
ENV PATH /usr/local/bin:${PATH}

# prepare python libraries
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

EXPOSE 5000
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]

# --- all
FROM base AS all

# prepare source code
COPY ./app ./app