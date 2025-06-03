output "public_ip" {
  description = "Public IP Adress of EC2"
  value       = data.aws_instance.flask_server.public_ip
}

output "instance_id" {
  description = "ID of EC2 running"
  value       = data.aws_instance.flask_server.id
}

output "key_pair_name" {
  description = "Key Pair Name is using"
  value       = var.key_pair
}
