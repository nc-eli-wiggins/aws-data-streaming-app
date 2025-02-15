resource "aws_cloudwatch_metric_alarm" "critical_error_alarm" {
  alarm_name = "critical_error_alarm" 
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods = 1
  period = 120
  metric_name = aws_cloudwatch_log_metric_filter.lambda_crit_error_filter.name
  namespace = aws_cloudwatch_log_metric_filter.lambda_crit_error_filter.metric_transformation[0].namespace
  statistic = "Sum"
  threshold = 1
  alarm_actions = [aws_sns_topic.critical_error_notifications.arn]
}

resource "aws_cloudwatch_log_metric_filter" "lambda_crit_error_filter" {
  name = "lambda_critical_error_filter"
  log_group_name = "/aws/lambda/${var.lambda_name}"
  pattern = "{ $.message = %Critical error% }"
  metric_transformation {
    name = "critical_error"
    namespace = "critical_errors"
    value = "1"
  }
}