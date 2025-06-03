terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

data "aws_instance" "flask_server" {
  instance_id = var.instance_id
}

resource "null_resource" "deploy_flask" {
  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = var.private_key
    host        = data.aws_instance.flask_server.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "docker stop flask-api || true",
      "docker rm flask-api || true",
      "docker rmi $(docker images -q tuan4886/flask-api) || true",
      "docker pull tuan4886/flask-api:latest",
      "docker run -d --name flask-api --env-file /home/ec2-user/.env -p 8080:8080 tuan4886/flask-api:latest"
    ]
  }
}
