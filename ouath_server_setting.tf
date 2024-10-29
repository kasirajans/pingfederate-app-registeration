# # resource "pingfederate_oauth_auth_server_settings_scopes_exclusive_scope" "oauthAuthServerSettingsScopesExclusiveScope" {
# #   for_each    = toset(local.scopes)
# #   dynamic     = false
# #   description = each.key
# #   name        = each.key
# # }


resource "pingfederate_oauth_server_settings" "oauthServerSettings" {
  authorization_code_entropy          = 30
  authorization_code_timeout          = 60
  bypass_activation_code_confirmation = false
  default_scope_description           = "default"
  device_polling_interval             = 5
  pending_authorization_timeout       = 600
  refresh_rolling_interval            = 0
  refresh_token_length                = 42
  scopes = [
    {
      name        = "address",
      description = "Address access",
      dynamic     = false
    },
    {
      name        = "phone",
      description = "Phone Number access",
      dynamic     = false
    },
    {
      name        = "openid",
      description = "OpenID Connect login",
      dynamic     = false
    },
    {
      name        = "profile",
      description = "Profile access",
      dynamic     = false
    },
    {
      name        = "email",
      description = "Email Address access",
      dynamic     = false
    }
  ]
  scope_groups = []
  exclusive_scopes = [
    for scope in local.scopes : {
      name        = scope
      description = scope
      dynamic     = false
    }
  ]
  exclusive_scope_groups = []
  disallow_plain_pkce                      = false
  include_issuer_in_authorization_response = false
  persistent_grant_lifetime                = 1
  persistent_grant_lifetime_unit           = "HOURS"
  persistent_grant_idle_timeout            = 1
  persistent_grant_idle_timeout_time_unit  = "HOURS"
  roll_refresh_token_values                = false
  refresh_token_rolling_grace_period       = 60
  persistent_grant_reuse_grant_types       = []
  persistent_grant_contract = {
    extended_attributes = [

        ]
  }
  bypass_authorization_for_approved_grants         = false
  allow_unidentified_client_ro_creds               = false
  allow_unidentified_client_extension_grants       = false
  token_endpoint_base_url                          = ""
  user_authorization_url                           = ""
  activation_code_check_mode                       = "AFTER_AUTHENTICATION"
  user_authorization_consent_page_setting          = "INTERNAL"
  atm_id_for_oauth_grant_management                = ""
  scope_for_oauth_grant_management                 = ""
  allowed_origins                                  = ["https://webapp.kraaj.local:8443"]
  track_user_sessions_for_logout                   = false
  par_reference_timeout                            = 60
  par_reference_length                             = 24
  par_status                                       = "ENABLED"
  client_secret_retention_period                   = 0
  jwt_secured_authorization_response_mode_lifetime = 600
}


# # resource "pingfederate_oauth_auth_server_settings_scopes_exclusive_scope" "oauthAuthServerSettingsScopesExclusiveScope" {
# #   for_each    = toset(local.scopes)
# #   dynamic     = false
# #   description = each.key
# #   name        = each.key
# # }
