FROM python:alpine

WORKDIR /app

# Copy dependencies file first so Docker can take advantage of cache
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]