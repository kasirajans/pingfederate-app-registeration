# provider "pingfederate" {
#   insecure_trust_all_tls = var.INSECURE_TRUST_ALL_TLS ? true : false
# }# provider "pingfederate" {
#   insecure_trust_all_tls = var.INSECURE_TRUST_ALL_TLS ? true : false
# }

terraform {
  required_version = ">=1.4"
  required_providers {
    pingfederate = {
      version = "~> 1.0.0"
      source  = "pingidentity/pingfederate"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "pingfederate" {
  username                            = var.PINGFEDERATE_PROVIDER_USERNAME
  password                            = var.PINGFEDERATE_PROVIDER_PASSWORD
  https_host                          = var.PINGFEDERATE_PROVIDER_HTTPS_HOST
  admin_api_path                      = var.PINGFEDERATE_PROVIDER_ADMIN_API_PATH
  product_version                     = "12.1"
}
