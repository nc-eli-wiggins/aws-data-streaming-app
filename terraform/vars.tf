variable "project_owner" {
    description = "Name to be used for project owner in resource tags"
    type = string
    default = "Martin C."
}

variable "project_owner_email" {
    description = "Email to be used for SNS notifications of critical errors"
    type = string
    default = "martinlambc@gmail.com"
}

variable "project_name" {
    type = string
    default = "data-streaming-app"
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

variable "secrets_arn" {
    description = "Retention date to be used in resource tags"
    type = string
    default = "arn:aws:secretsmanager:eu-west-2:340752809785:secret:Guardian-API-Key-MzSRM5"
}