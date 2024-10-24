variable "env" {
  description = "The environment (e.g., US/Prod)"
  type        = string
}

variable "yaml_file" {
  description = "The name of the YAML file"
  type        = string
}

variable "PINGFEDERATE_AUD" {
  type = string
}