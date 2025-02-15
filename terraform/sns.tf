resource "aws_sns_topic" "critical_error_notifications" {
  name = "critical_errors"
}


resource "aws_sns_topic_subscription" "crit_error_subscription" {
  topic_arn = aws_sns_topic.critical_error_notifications.arn
  protocol = "email"
  endpoint = var.project_owner_email
}