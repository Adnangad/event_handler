FROM python:3.13-slim AS builder

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local
COPY --from=builder /app/requirements.txt /app/

WORKDIR /app

COPY --chown=appuser:appuser . .

ENV JWT_ALGORITHM="HS256"
ENV JWT_EXPIREY=604800
ENV DEBUG=0
ENV DJANGO_ALLOWED_HOSTS=localhost

USER appuser

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "event_handler_backend.wsgi:application"]
