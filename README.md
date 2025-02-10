# aws-data-streaming-app


## Prerequisites

- An AWS IAM user with CLI access keys
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Terraform](https://developer.hashicorp.com/terraform/install)
- A [Guardian API access key](https://open-platform.theguardian.com/access/)
- Python 3.12.3

## Setup Instructions

1. **Clone the repo:**  
   ```bash  
   git clone https://github.com/FloatingBrioche/aws-data-streaming-app.git
   cd aws-data-streaming-app 
   ``` 

2. **Add your Guardian API key to your AWS Secrets Manager**
    ```bash
    aws secretsmanager create-secret --name Guardian-API-Key --description "Access key for Guardian API." --secret-string "[ADD YOUR API KEY HERE]"
    ```

3. **Create your Terraform State Bucket**
    ```bash
    aws s3api create-bucket \
    --bucket [ADD YOUR BUCKET NAME] \
    --region [ADD YOUR REGION] \
    --create-bucket-configuration LocationConstraint=[YOUR REGION]
    ```

4. **Update the Terraform vars in the [terraform-perm directory](./terraform-perm/vars.tf)**


5. **Add your AWS access key and secret access key to the repo secrets**

- Go to Settings > Secrets and variables > Actions.
- Click New repository secret.
- Use AWS_ACCESS_KEY and AWS_SECRET__ACCESS_KEY as the secrets names, adding your own values for the secrets themselves.
