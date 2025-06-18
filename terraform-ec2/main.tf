terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_instance" "flask_server" {
  ami                         = var.ami_id
  instance_type               = "t2.micro"
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [var.sg_id]
  key_name                    = var.key_pair
  associate_public_ip_address = true

  user_data = <<-EOF
    #!/bin/bash
    echo "Starting Docker and Docker Compose installation..."

    # Update existing packages
    sudo yum update -y
    
    # Install Docker
    sudo yum install docker -y
    
    # Start Docker service
    sudo systemctl start docker
    
    # Enable Docker to run on system startup
    sudo systemctl enable docker
    
    # Add ec2-user to the docker group so that sudo is not required when running docker commands
    sudo usermod -aG docker ec2-user
    
    # Install Docker Compose (Version 1.29.2 is a popular version, you can change it)
    # Get Docker Compose from GitHub Releases
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    
    # Grant execute permissions to Docker Compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    # Create a symbolic link to run docker-compose from anywhere
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
    
    echo "Docker and Docker Compose installed successfully."
  EOF

  tags = {
    Name = "FlaskServer"
  }
}


