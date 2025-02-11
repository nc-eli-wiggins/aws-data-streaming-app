variable "state_bucket" {
    description = "S3 bucket name for storing Terraform state file"
    type = string
    default = "mc-guardian-data-streaming-terraform-state-bucket "
}

variable "project_owner" {
    description = "Name to be used for project owner in resource tags"
    type = string
    default = "Martin C."
}

variable "department" {
    description = "Department name to be used in resource tags"
    type = string
    default = "Data Engineering"
}

variable "retention_date" {
    description = "Retention date to be used in resource tags"
    type = string
    default = "2025-03-31"
}