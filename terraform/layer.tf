resource "null_resource" "create_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../layer_requirements.txt -t ${path.module}/../layer/python"
  }

  triggers = {
    dependencies = filemd5("${path.module}/../layer_requirements.txt")
  }
}


data "archive_file" "layer" {
    type = "zip"
    source_dir =  "${path.module}/../layer" 
    output_path =  "${path.module}/../zip_files/layer.zip"

    depends_on = [ null_resource.create_dependencies ]
}


resource "aws_lambda_layer_version" "dependencies" {
  layer_name = "requests_boto3_layer"
  s3_bucket  = aws_s3_object.layer_code.bucket
  s3_key     = aws_s3_object.layer_code.key
}