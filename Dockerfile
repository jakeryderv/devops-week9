FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8501

# A writable working directory also preserves the local SQLite fallback.
RUN useradd --uid 10001 --user-group --create-home --shell /usr/sbin/nologin appuser \
    && chown appuser:appuser /app

USER appuser

CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501"]
