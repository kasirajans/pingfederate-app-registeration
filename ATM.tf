resource "pingfederate_oauth_access_token_manager" "jwt" {
  for_each   = { for atm in local.all_atms_check_contract_not_null : atm.pfname => atm }
  #ping ATM Schema dosnt support managerID with _. Removing _ value
  manager_id = replace(each.value.pfname, "_", "")
  name       = each.value.pfname
  plugin_descriptor_ref = {
    id = "com.pingidentity.pf.access.token.management.plugins.JwtBearerAccessTokenManagementPlugin"
  }
  configuration = {
    tables = [
      {
        name = "Symmetric Keys"
        rows = [

        ]
      },
      {
        name = "Certificates"
        rows = []
      }
    ]
    fields = [
      {
        name  = "Token Lifetime"
        value = lookup(each.value, "TokenLifetime", var.ATMTokenLifetime)
      },
      {
        name  = "Use Centralized Signing Key"
        value = lookup(each.value, "UseCentralizedSigningKey", var.UseCentralizedSigningKey)
      },
      {
        name  = "JWS Algorithm"
        value = "RS256"
      },
      {
        name  = "Active Symmetric Key ID"
        value = ""
      },
      {
        name  = "Active Signing Certificate Key ID"
        value = ""
      },
      {
        name  = "JWE Algorithm"
        value = ""
      },
      {
        name  = "JWE Content Encryption Algorithm"
        value = ""
      },
      {
        name  = "Active Symmetric Encryption Key ID"
        value = ""
      },
      {
        name  = "Asymmetric Encryption Key"
        value = ""
      },
      {
        name  = "Asymmetric Encryption JWKS URL"
        value = ""
      },
      {
        name  = "Enable Token Revocation"
        value = "false"
      },
      {
        name  = "Include Key ID Header Parameter"
        value = "true"
      },
      {
        name  = "Default JWKS URL Cache Duration"
        value = "720"
      },
      {
        name  = "Include JWE Key ID Header Parameter"
        value = "true"
      },
      {
        name  = "Client ID Claim Name"
        value = ""
      },
      {
        name  = "Scope Claim Name"
        value = ""
      },
      {
        name  = "Space Delimit Scope Values"
        value = "true"
      },
      {
        name  = "Authorization Details Claim Name"
        value = "authorization_details"
      },
      {
        name  = "Issuer Claim Value"
        value = var.PINGFEDERATE_ISSUER
      },
      {
        name  = "Audience Claim Value"
        value = var.PINGFEDERATE_AUD
      },
      {
        name  = "JWT ID Claim Length"
        value = "46"
      },
      {
        name  = "Access Grant GUID Claim Name"
        value = ""
      },
      {
        name  = "JWKS Endpoint Path"
        value = ""
      },
      {
        name  = "JWKS Endpoint Cache Duration"
        value = "720"
      },
      {
        name  = "Include Issued At Claim",
        value = "true"
      },
      {
        name  = "Expand Scope Groups"
        value = "false"
      },
      {
        name  = "Type Header Value"
        value = ""
      }
    ]
  }
# Create contract based on ATM.tf file attribute_contract -> attributes by select keys
  attribute_contract = {
    coreAttributes = []
    extended_attributes = [for attr in each.value.attributes :
      {
        name         = keys(attr)[0] # Extract the claim key names
        multi_valued = false
      }
 ]
  }
  selection_settings = {
    resource_uris = []
  }
  access_control_settings = {
    restrict_clients = false
  }
  session_validation_settings = {
    check_valid_authn_session       = false
    check_session_revocation_status = false
    update_authn_session_activity   = false
    include_session_id              = false
  }
  # dynamic "attribute_contract.core_attributes"{
  #   for_each= each.value.extended_attributes
  #   content{
  #     name = extended_attributes.name
  #     multi_valued = false
  #   }
  # }
}

resource "pingfederate_oauth_access_token_mapping" "oauthAccessTokenMapping" {
  for_each = { for atm, obj in pingfederate_oauth_access_token_manager.jwt : atm => obj }
  access_token_manager_ref = {
    id = each.value.id
  }
  #Check for LDAP_DATA_STORE value exists in ATM claims Contract fullfilment requests if exists add default ldap_attribute_source
  attribute_sources = length(local.all_atms_check_contract_not_null_EXPRESSION) > 0 ? flatten([local.ldap_attribute_source_for_machine]) : []

# Get Contract mapping and fullfillment
# Check whther clm and LDAP_DATA_STORE in attr 
# if exists replace clm value with local.clm expression else pass default attr
  attribute_contract_fulfillment = {
    for attr in lookup(local.all_atms_check_contract_not_null_map, each.key, {}).attributes : keys(attr)[0] => {
      source = attr[keys(attr)[0]].source
      value  = attr[keys(attr)[0]].value
    }
  }


  context = {
    type = "CLIENT_CREDENTIALS"
  }

  issuance_criteria = {
    conditional_criteria = []
  }
}