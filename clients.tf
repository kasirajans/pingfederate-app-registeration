resource "pingfederate_oauth_client" "oauthClient" {
  for_each = { for idx, client in local.clients_with_formatted_fields : client.client_id => client }
  # manager_id = replace(each.value.name,"_","")
  depends_on                       = [pingfederate_oauth_server_settings.oauthServerSettings]
  name                             = "${each.value.pfname}-tf"
  client_id                        = each.value.client_id
  description                      = each.value.description
  persistent_grant_expiration_time = 1
  persistent_grant_expiration_type = "OVERRIDE_SERVER_DEFAULT"
  persistent_grant_expiration_time_unit = "MINUTES"
  # client_id = each.value.name
  grant_types = each.value.grantTypes
  allow_authentication_api_init = false
  bypass_approval_page          = true
  client_auth = {
    type   = "SECRET"
    secret = each.value.client_secret
  }
  enabled                                         = true
  redirect_uris                                   = []
  require_jwt_secured_authorization_response_mode = false
  require_pushed_authorization_requests           = false
  require_proof_key_for_code_exchange             = false
  require_signed_requests                         = false
  restrict_scopes                                 = false
  restricted_scopes = [
  ]
  exclusive_scopes = lookup(each.value, "scopes", null)
  default_access_token_manager_ref = {
    # Filter the list to pick only the entry where first_part_of_name is "each.value.pfname"
    id = ([for manager in local.pf_ATM_first_part_of_name : manager if split("_", manager.name)[0] == split("_", each.value.pfname)[0]][0]).id
    #  id = length(split("_", each.value.pfname)) > 2 ? join("", slice(split("_", each.value.pfname), 0, 2)) : length(split("_", each.value.pfname)) > 1 ? join("", slice(split("_", each.value.pfname), 0, 1)) : each.value.pfname
  }
  restrict_to_default_access_token_manager = false
  validate_using_all_eligible_atms         = false
}
