# aws-data-streaming-app


## Prerequisites

- An AWS IAM user with CLI access keys
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Terraform](https://developer.hashicorp.com/terraform/install)
- A [Guardian API access key](https://open-platform.theguardian.com/access/)
- Python 3.12.3

## Setup Instructions

1. Add your Guardian API key to your AWS Secrets Manager
```bash
aws secretsmanager create-secret --name Guardian-API-Key --description "Access key for Guardian API." --secret-string "[ADD YOUR API KEY HERE]"
```