resource "null_resource" "create_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../layer_requirements.txt -t ${path.module}/../layer/python"
  }

  triggers = {
    dependencies = filemd5("${path.module}/../layer_requirements.txt")
  }
}


data "archive_file" "lambda" {
    type        = "zip"
    source_dir  = "${path.module}/../lambda_app"
    output_path = "${path.module}/../zip_files/lambda_app.zip"

}


data "archive_file" "layer" {
    type = "zip"
    source_dir =  "${path.module}/../layer" 
    output_path =  "${path.module}/../zip_files/layer.zip"

    depends_on = [ null_resource.create_dependencies ]
}

