output "public_ip" {
  description = "Public IP của EC2"
  value       = aws_instance.flask_server.public_ip
}
