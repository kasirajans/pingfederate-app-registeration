# Input variables for region and environment
variable "region" {
  description = "The region to deploy the resources (e.g., US, EU)"
  type        = string
}

variable "PINGFEDERATE_ISSUER" {
  description = "PingFedrate Issuer"
  type        = string
}

variable "PINGFEDERATE_AUD" {
  description = "PingFederate AUD"
  type        = string
}

variable "ATMTokenLifetime" {
  description = "PingFederate AUD"
  type        = string
  default     = "60"
}

variable "UseCentralizedSigningKey" {
  description = "PingFederate AUD"
  type        = bool
  default     = true
}

variable "env" {
  description = "PingFederate AUD"
  type        = string
}

variable "PINGFEDERATE_PROVIDER_HTTPS_HOST" {
  description = "PingDirectory REST API URL"
  type        = string
}

variable "PINGFEDERATE_PROVIDER_USERNAME" {
  description = "PingDirectory UserName"
}

variable "PINGFEDERATE_PROVIDER_PASSWORD" {
  description = "PingDirectory Password"
  
}

variable "PINGFEDERATE_PROVIDER_ADMIN_API_PATH" {
  description = "PingDirectory Admin API Path"
  type        = string
  
}

variable "PINGFEDERATE_LDAP_DATASTORE" {
  description = "PingDirectory LDAP Datastore"
  type        = string
  
}

variable "machine_base_dn_value" {
  description = "The base DN for the LDAP configuration"
  type        = string
}