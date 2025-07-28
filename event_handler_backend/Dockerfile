# Python Version
FROM python:3.13-slim AS builder

# create app dir
RUN mkdir /app

WORKDIR /app

ARG JWT_SECRET
ARG SECRET_KEY


ENV JWT_SECRET=$JWT_SECRET
ENV SECRET_KEY=$SECRET_KEY
ENV JWT_ALGORITHM="HS256"
ENV JWT_EXPIREY=604800
ENV DEBUG=0
ENV DJANGO_ALLOWED_HOSTS=localhost  


RUN pip install --upgrade pip

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim

RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app
 
# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 

WORKDIR /app
 
# Copy application code
COPY --chown=appuser:appuser . .
 
# Set environment variables to optimize Python
ENV JWT_SECRET=$JWT_SECRET
ENV SECRET_KEY=$SECRET_KEY
ENV JWT_ALGORITHM="HS256"
ENV JWT_EXPIREY=604800
ENV DEBUG=0
ENV DJANGO_ALLOWED_HOSTS=localhost
 
# Switch to non-root user
USER appuser

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "event_handler_backend.wsgi:application"]