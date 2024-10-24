terraform {
  required_version = ">=1.1"
  required_providers {
    pingfederate = {
      version = "~> 0.13.0"
      source  = "pingidentity/pingfederate"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}


provider "external" {}

data "external" "yaml_data" {
  program = [
    "python",
    "${path.module}/scripts/read_yaml.py",
    "--env", var.env,
    "--file", var.yaml_file
  ]
}


locals {

  #Read the JSON file
  python_payload = jsondecode(data.external.yaml_data.result.resources)
# Add formatted client name with "tf" at the end and prepend "0oapf" to client_id
  clients_with_formatted_fields = [
    for client in local.python_payload : merge(
      client,
      {
        # Append "tf" to client.name
        "pfname"      = format("%s%s", client.name, "_tf"),
        # Prepend "0oapf" to client_id (randomly generated or existing)
        "client_id" = format("0oa14%s", random_string.client_ids[client.name].id)
      }
    )
  ]

}
# Generate random strings (client_ids) for clients that do not already have a ClientId
resource "random_string" "client_ids" {
  for_each    = { for client in local.python_payload : client.name => client }

  length  = 16    # Length of the random string
  special = false # Include special characters
  upper   = true  # Include uppercase letters
  lower   = true  # Include lowercase letters
  numeric = true  # Include numbers
}
# output "merged_data" {
#   value = local.python_payload
# }

