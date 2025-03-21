### Resource: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sqs_queue


resource "aws_sqs_queue" "guardian_content_queue" {
  name                      = "guardian_content"
  message_retention_seconds = 259200
  receive_wait_time_seconds = 5
}


