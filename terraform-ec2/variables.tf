variable "aws_region" {
  description = "AWS Region"
  type        = string
}

variable "ami_id" {
  description = "AMI ID (Amazon Linux 2)"
  type        = string
  default     = "ami-0fa377108253bf620" # ap-southeast-1
}

variable "subnet_id" {
  description = "Subnet ID để gán EC2"
  type        = string
}

variable "sg_id" {
  description = "Security Group đã được tạo sẵn"
  type        = string
}

variable "key_pair" {
  description = "Tên Key Pair EC2"
  type        = string
}
