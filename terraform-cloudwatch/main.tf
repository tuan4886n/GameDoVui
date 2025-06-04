terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Create a Log Group on CloudWatch to store EC2 logs
resource "aws_cloudwatch_log_group" "flask_logs" {
  name              = "flask-api-log-group"
  retention_in_days = 5 # Delete log after 5 days
}

# Create IAM policy for EC2, enable AssumeRole to use CloudWatch
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

# Create an IAM Role for EC2 to have access to CloudWatch
resource "aws_iam_role" "cloudwatch_role" {
  name               = "CloudWatchEC2Role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Attach the `CloudWatchAgentServerPolicy` Policy to the IAM Role
resource "aws_iam_policy_attachment" "cloudwatch_policy" {
  name       = "attach-cloudwatch-policy"
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
  roles      = [aws_iam_role.cloudwatch_role.name]
}

# Create Instance Profile and assign Role to EC2
resource "aws_iam_instance_profile" "cloudwatch_profile" {
  name = "CloudWatchEC2Profile"
  role = aws_iam_role.cloudwatch_role.name
}

# Set up CloudWatch alerts when EC2 CPU exceeds 80%
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "EC2-High-CPU"
  comparison_operator = "GreaterThanThreshold" # Check if threshold is exceeded
  evaluation_periods  = 2                      # CPU test in 2 cycles
  metric_name         = "CPUUtilization"       # Monitor CPU usage
  namespace           = "AWS/EC2"              # Belongs to EC2 metrics group
  statistic           = "Average"              # Use the average value
  threshold           = 80                     # Alarm when CPU exceeds 80%
  period              = 300                    # Check every 5 minutes (300 seconds)
  alarm_actions       = [var.sns_topic_arn]    # Send warning via SNS
}
