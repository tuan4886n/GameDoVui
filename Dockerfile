FROM python:alpine

WORKDIR /app

# Copy dependencies file first so Docker can take advantage of cache
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]