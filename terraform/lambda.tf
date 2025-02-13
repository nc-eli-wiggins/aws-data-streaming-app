data "archive_file" "lambda" {
    type        = "zip"
    source_dir  = "${path.module}/../lambda_app"
    output_path = "${path.module}/../zip_files/lambda_app.zip"

}


resource "aws_lambda_function" "data_streaming_lambda" {
  function_name    = "lambda_function"
  source_code_hash = data.archive_file.lambda.output_base64sha256
  s3_bucket        = aws_s3_bucket.code_bucket.bucket
  s3_key           = aws_s3_object.lambda_code.key
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  timeout          = 180
  layers           = [aws_lambda_layer_version.dependencies.arn]

  depends_on = [aws_s3_object.lambda_code, aws_s3_object.lambda_layer]
}