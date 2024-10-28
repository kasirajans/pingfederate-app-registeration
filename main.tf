# Dynamically load the merged JSON file based on the region and environment
data "local_file" "merged_json" {
  filename = "${path.module}/${var.region}_${var.env}_merged_output.json"
}

# Decode the JSON file
locals {
  merged_data                      = jsondecode(data.local_file.merged_json.content)
  all_atms_check_contract_not_null = [for key in local.merged_data["ATM"] : merge(key, contains(keys(key), "attributes") ? {} : { "attributes" = [{ "cid" = { "source" = { "type" = "CONTEXT" }, "value" = "ClientId" } }] })]
  all_atms_check_contract_not_null_EXPRESSION                   = [for key in local.all_atms_check_contract_not_null : contains(keys(key), "attributes") ? key["attributes"] : []]
  all_atms_check_contract_not_null_attributeContractFulfillment = [for key in local.all_atms_check_contract_not_null : contains(keys(key), "attributes") ? key["attributes"] : []]
  # Convert the list to a map using 'pfname' as the key
  all_atms_check_contract_not_null_map = {
    for atm in local.all_atms_check_contract_not_null : atm.pfname => atm
  }

  ldap_attribute_source_for_machine = {
    ldap_attribute_source = {
      base_dn        = var.machine_base_dn_value
      search_scope   = "SUBTREE"
      search_filter  = "cid=$${client_id}"
      id             = "LdapMachine"
      data_store_ref = { id = var.PINGFEDERATE_LDAP_DATASTORE }
      search_attributes = [
        "Subject DN",
        "clm"
      ]
      description = "Used to get M2M claim from PingDirectory"
      type        = "LDAP"
    }
  }

  # Add formatted client name with "tf" at the end and prepend "0oapf" to client_id
  clients_with_formatted_fields = [
    for client in local.merged_data["clients"] : merge(
      client,
      {
        # Prepend "0oapf" to client_id (randomly generated or existing)
        "client_id" = "${format("0oa14%s", lookup(random_string.clientId, client.pfname, {}).result)}",
        # Include generated password
        "client_secret" = lookup(random_password.client_password, client.pfname, {}).result
      }
    )
  ]
  scopes = local.merged_data["scopes"]
  # scopes= [for scope in local.merged_data["scopes"] : {
  #   name = scope.name
  #   description = scope.description
  # }]

  pf_ATM_first_part_of_name=[
    for manager in pingfederate_oauth_access_token_manager.jwt : {
      id = manager.id
      name = manager.name
      first_part_of_name = element(split("_", manager.name), 0)
    }
  ]
  PingDirectoryDefaultLdapEnv_machine = { ldap_attribute_source = merge({ data_store_ref = { id = var.PINGFEDERATE_LDAP_DATASTORE } }, local.ldap_attribute_source_for_machine.ldap_attribute_source) }
  expression = {
    Numeric_JWT_Date              = "@org.jose4j.jwt.NumericDate@now().getValue()"
    JSONParser_LDAP_Get_country   = "new org.json.simple.parser.JSONParser().parse(#this.get('ds.LdapMachine.clm')).get('country')"
    JSONParser_LDAP_Get_partnerID = "new org.json.simple.parser.JSONParser().parse(#this.get('ds.LdapMachine.clm')).get('partnerID')"
    JSONParser_LDAP_Get_language  = "new org.json.simple.parser.JSONParser().parse(#this.get('ds.LdapMachine.clm')).get('language')"
    JSONParser_LDAP_Get_clm       = "new org.json.simple.parser.JSONParser().parse(#this.get('ds.LdapMachine.clm'))"
  }
}

# Generate random strings (client_ids) for clients that do not already have a ClientId
resource "random_string" "clientId" {
  for_each = { for client in local.merged_data["clients"] : client.pfname => client }

  length  = 16    # Length of the random string
  special = false # Include special characters
  upper   = true  # Include uppercase letters
  lower   = true  # Include lowercase letters
  numeric = true  # Include numbers
}

# Generate random passwords for each client
resource "random_password" "client_password" {
  for_each = { for client in local.merged_data["clients"] : client.pfname => client }

  length           = 20   # Length of the generated password
  special          = true # Include special characters
  upper            = true # Include uppercase letters
  lower            = true # Include lowercase letters
  numeric          = true # Include numbers
  override_special = "_"  # Special characters allowed
}