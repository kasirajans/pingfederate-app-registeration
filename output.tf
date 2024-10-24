# output "INSECURE_TRUST_ALL_TLS" {
#   value = var.INSECURE_TRUST_ALL_TLS
# }


output "PINGFEDERATE_AUD" {
  value = var.PINGFEDERATE_AUD
}

# Output the updated clients object with client_ids
output "updated_clients" {
  value = local.clients_with_formatted_fields
}