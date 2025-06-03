variable "aws_region" {
  description = "AWS region where EC2 is running"
  type        = string
}

variable "instance_id" {
  description = "Instance ID EC2 "
  type        = string
}

variable "key_pair" {
  description = "Key Pair Name to SSH connect EC2"
  type        = string
}

variable "private_key" {
  description = "Private key for SSH"
  type        = string
}
