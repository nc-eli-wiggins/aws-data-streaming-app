data "archive_file" "lambda" {
    type        = "zip"
    source_dir  = "${path.module}/../lambda_app"
    output_path = "${path.module}/../zip_files/lambda_app.zip"
}

data "archive_file" "layer" {
  type = "zip"
  source_dir =  "${path.module}/../layer" 
  output_path =  "${path.module}/../zip_files/layer.zip"
}