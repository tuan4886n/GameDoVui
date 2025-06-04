variable "aws_region" {
  description = "AWS region to deploy CloudWatch"
  type        = string
}

variable "instance_id" {
  description = "Instance ID EC2 "
  type        = string
}

variable "sns_topic_arn" {
  description = "ARN của SNS Topic dùng để gửi cảnh báo CPU"
  type        = string
}
