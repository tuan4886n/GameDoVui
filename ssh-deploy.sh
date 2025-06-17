#!/bin/bash

set -e

# Environment variables
: "${EC2_IP:?Bạn chưa khai báo EC2_IP}"
: "${PEM_KEY_PATH:?Bạn chưa khai báo PEM_KEY_PATH (.pem file path)}"
: "${EC2_USER:=ec2-user}"  # default is ec2-user

echo "Deploying to $EC2_USER@$EC2_IP using $DOCKER_IMAGE..."

# Copy .env environment variable to EC2
if [ -f .env ]; then
  echo "Sending .env..."
  scp -i "$PEM_KEY_PATH" -o StrictHostKeyChecking=no .env "$EC2_USER@$EC2_IP:/home/$EC2_USER/flask-app/.env"
fi

# Gửi docker-compose nếu có
if [ -f docker-compose.yml ]; then
  echo "Sending docker-compose.yml..."
  scp -i "$PEM_KEY_PATH" -o StrictHostKeyChecking=no docker-compose.yml "$EC2_USER@$EC2_IP:/home/$EC2_USER/flask-app/"
fi

# Chạy lệnh deploy từ xa
ssh -i "$PEM_KEY_PATH" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_IP" bash << EOF
  set -e
  cd ~/flask-app 

  echo "📥 Pulling latest image..."
  docker-compose pull

  echo "🛑 Stopping old container..."
  docker-compose down

  echo "🚀 Starting container with Compose..."
  docker-compose up -d

  echo "✅ Deploy done via docker-compose!"
EOF