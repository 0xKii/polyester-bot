# Polyester API schemas

Decoded ConnectRPC `FileDescriptorProto` dumps pulled from the app's JS bundles.

All 35 service/type schemas consolidated into this single file.


## `auth_v1_address_book`

```
// auth/v1/address_book.proto  package=auth.v1
enum AccountScopeType {
  SCOPE_UNSPECIFIED = 0;
  SCOPE_ROOT = 1;
  SCOPE_SUBACCOUNT = 2;
}
enum AddressBookEntryKind {
  ENTRY_KIND_UNSPECIFIED = 0;
  EXTERNAL_CHAIN = 1;
  INTERNAL_ACCOUNT = 2;
}
enum InternalWhitelistResolutionStatus {
  INTERNAL_WHITELIST_RESOLUTION_UNSPECIFIED = 0;
  INTERNAL_WHITELIST_RESOLVED = 1;
  INTERNAL_WHITELIST_UNRESOLVED = 2;
}
enum DestinationWhitelistStatus {
  DESTINATION_WHITELIST_STATUS_UNSPECIFIED = 0;
  DESTINATION_NOT_WHITELISTED = 1;
  DESTINATION_WHITELIST_ACTIVE = 2;
  DESTINATION_WHITELIST_UNRESOLVED = 3;
}
enum TransferCounterpartyDirection {
  TRANSFER_COUNTERPARTY_DIRECTION_UNSPECIFIED = 0;
  DEPOSIT_FROM = 1;
  WITHDRAW_TO = 2;
  INTERNAL_TRANSFER_FROM = 3;
  INTERNAL_TRANSFER_TO = 4;
}
message AccountScopeRef {
  optional .auth.v1.AccountScopeType scope_type = 1;
  optional 6 root_account_id = 2;
  optional 6 subaccount_id = 3;
}
message AddressBook {
  optional .auth.v1.AccountScopeRef scope = 1;
  optional .auth.v1.SubaccountRole caller_role = 2;
  optional 9 label = 3;
  optional 9 owner_username = 4;
  optional 9 smart_account_address = 5;
}
message ExternalWithdrawAddress {
  optional 13 polychain_chain_id = 1;
  optional 9 address = 2;
}
message InternalTransferAccount {
  optional 6 root_account_id = 1;
  optional 6 target_account_id = 2;
  optional .auth.v1.AccountScopeType target_scope_type = 3;
  optional 9 smart_account_address = 4;
  optional 9 root_username = 5;
  optional 9 subaccount_label = 6;
}
message AddressBookTag {
  optional 6 tag_id = 1;
  optional .auth.v1.AccountScopeRef scope = 2;
  optional 9 name = 3;
  optional 9 color = 4;
  optional .google.protobuf.Timestamp created_at = 5;
  optional .google.protobuf.Timestamp updated_at = 6;
}
message AddressBookTagSummary {
  optional 6 tag_id = 1;
  optional 9 name = 2;
  optional 9 color = 3;
}
message AddressBookEntry {
  optional 6 address_book_entry_id = 1;
  optional .auth.v1.AccountScopeRef scope = 2;
  optional .auth.v1.AddressBookEntryKind kind = 3;
  optional 9 label = 4;
  optional 9 note = 5;
  optional .google.protobuf.Timestamp created_at = 6;
  optional .google.protobuf.Timestamp updated_at = 7;
  optional .auth.v1.ExternalWithdrawAddress external = 20;
  optional .auth.v1.InternalTransferAccount internal = 21;
  repeated .auth.v1.AddressBookTag tags = 30;
  optional 4 revision = 31;
}
message AddressBookEntriesView {
  repeated .auth.v1.ExternalAddressBookEntry external = 1;
  repeated .auth.v1.InternalAddressBookEntry internal = 2;
}
message ExternalAddressBookEntry {
  optional 6 address_book_entry_id = 1;
  optional .auth.v1.AccountScopeRef scope = 2;
  optional 9 label = 3;
  optional 9 note = 4;
  repeated 6 tag_ids = 5;
  optional .auth.v1.DestinationWhitelistStatus whitelist_status = 6;
  optional 13 polychain_chain_id = 7;
  optional 9 address = 8;
  optional .google.protobuf.Timestamp created_at = 9;
  optional .google.protobuf.Timestamp updated_at = 10;
  optional 4 revision = 11;
}
message InternalAddressBookEntry {
  optional 6 address_book_entry_id = 1;
  optional .auth.v1.AccountScopeRef scope = 2;
  optional 9 label = 3;
  optional 9 note = 4;
  repeated 6 tag_ids = 5;
  optional .auth.v1.DestinationWhitelistStatus whitelist_status = 6;
  optional 6 root_account_id = 7;
  optional 6 target_account_id = 8;
  optional .auth.v1.AccountScopeType target_scope_type = 9;
  optional 9 smart_account_address = 10;
  optional 9 root_username = 11;
  optional 9 subaccount_label = 12;
  optional .google.protobuf.Timestamp created_at = 13;
  optional .google.protobuf.Timestamp updated_at = 14;
  optional 4 revision = 15;
}
message TransferCounterparty {
  optional 6 counterparty_id = 1;
  optional .auth.v1.AccountScopeRef scope = 2;
  optional .auth.v1.TransferCounterpartyDirection direction = 3;
  optional .auth.v1.AddressBookEntryKind kind = 4;
  optional 8 saved = 5;
  optional 6 address_book_entry_id = 6;
  optional 4 use_count = 7;
  optional .google.protobuf.Timestamp first_seen_at = 8;
  optional .google.protobuf.Timestamp last_seen_at = 9;
  optional .auth.v1.ExternalWithdrawAddress external = 20;
  optional .auth.v1.InternalTransferAccount internal = 21;
}
message AddressBookRecentDestinationsView {
  repeated .auth.v1.ExternalRecentDestination external = 1;
  repeated .auth.v1.InternalRecentDestination internal = 2;
}
message ExternalRecentDestination {
  optional .auth.v1.AccountScopeRef scope = 1;
  optional .auth.v1.TransferCounterpartyDirection last_direction = 2;
  optional 8 saved = 3;
  optional 6 address_book_entry_id = 4;
  optional 4 use_count = 5;
  optional .google.protobuf.Timestamp last_seen_at = 6;
  optional 13 polychain_chain_id = 7;
  optional 9 address = 8;
}
message InternalRecentDestination {
  optional .auth.v1.AccountScopeRef scope = 1;
  optional .auth.v1.TransferCounterpartyDirection last_direction = 2;
  optional 8 saved = 3;
  optional 6 address_book_entry_id = 4;
  optional 4 use_count = 5;
  optional .google.protobuf.Timestamp last_seen_at = 6;
  optional 6 root_account_id = 7;
  optional 6 target_account_id = 8;
  optional .auth.v1.AccountScopeType target_scope_type = 9;
  optional 9 smart_account_address = 10;
  optional 9 root_username = 11;
  optional 9 subaccount_label = 12;
}
message InternalTransferWhitelistEntry {
  optional 6 entry_id = 1;
  optional .auth.v1.AccountScopeRef scope = 2;
  optional 6 root_account_id = 3;
  optional 6 target_account_id = 4;
  optional .auth.v1.AccountScopeType target_scope_type = 5;
  optional 9 smart_account_address = 6;
  optional 9 root_username = 7;
  optional 9 subaccount_label = 8;
  optional .google.protobuf.Timestamp created_at = 9;
  optional .google.protobuf.Timestamp updated_at = 10;
  optional .auth.v1.InternalWhitelistResolutionStatus resolution_status = 11;
}
message MirroredWithdrawWhitelistEntry {
  optional 9 canonical_address = 1;
  optional 9 raw_address_hex = 2;
  optional .google.protobuf.Timestamp updated_at = 5;
  optional 13 polychain_chain_id = 6;
}
message WithdrawWhitelistView {
  optional .auth.v1.AccountScopeRef scope = 1;
  optional 8 external_whitelist_required = 2;
  repeated .auth.v1.MirroredWithdrawWhitelistEntry active_entries = 3;
  optional 8 internal_whitelist_required = 4;
}
message TransferDestination {
  optional .auth.v1.AccountScopeRef scope = 1;
  optional .auth.v1.AddressBookEntryKind kind = 2;
  optional 8 saved = 3;
  optional 8 whitelisted = 4;
  optional .auth.v1.DestinationWhitelistStatus whitelist_status = 5;
  optional .auth.v1.AddressBookEntry address_book_entry = 6;
  optional .auth.v1.ExternalWithdrawAddress external = 20;
  optional .auth.v1.InternalTransferAccount internal = 21;
  optional .google.protobuf.Timestamp whitelist_updated_at = 31;
}
message ListAddressBooksRequest {
}
message ListAddressBooksResponse {
  repeated .auth.v1.AddressBook books = 1;
}
message ListAddressBookEntriesRequest {
  optional 6 subaccount_id = 1;
  optional .auth.v1.AddressBookEntryKind kind = 2;
  optional 13 limit = 3;
  optional 9 page_token = 4;
}
message ListAddressBookEntriesResponse {
  repeated .auth.v1.AddressBookEntry entries = 1;
  optional 9 next_page_token = 2;
}
message CreateAddressBookEntryRequest {
  optional 6 subaccount_id = 1;
  optional 9 label = 2;
  optional 9 note = 3;
  optional .auth.v1.ExternalWithdrawAddress external = 10;
  optional .auth.v1.RequestedInternalTransferAccount internal = 11;
  repeated 6 tag_ids = 4;
  repeated .auth.v1.AddressBookTagInput new_tags = 5;
}
message RequestedInternalTransferAccount {
  optional 9 smart_account_address = 1;
}
message CreateAddressBookEntryResponse {
  optional .auth.v1.AddressBookEntry entry = 1;
}
message AddressBookEntryUpdateSpec {
  optional 9 label = 1;
  optional 9 note = 2;
  repeated 6 tag_ids = 3;
  repeated .auth.v1.AddressBookTagInput new_tags = 4;
}
message UpdateAddressBookEntryRequest {
  optional 6 address_book_entry_id = 1;
  optional .auth.v1.AddressBookEntryUpdateSpec entry = 2;
  optional .google.protobuf.FieldMask update_mask = 3;
  optional 4 expected_revision = 4;
}
message UpdateAddressBookEntryResponse {
  optional .auth.v1.AddressBookEntry entry = 1;
}
message AddressBookTagInput {
  optional 9 name = 1;
  optional 9 color = 2;
}
message DeleteAddressBookEntryRequest {
  optional 6 address_book_entry_id = 1;
}
message DeleteAddressBookEntryResponse {
}
message CopyAddressBookEntryRequest {
  optional 6 address_book_entry_id = 1;
  optional 6 target_subaccount_id = 2;
}
message CopyAddressBookEntryResponse {
  optional .auth.v1.AddressBookEntry entry = 1;
}
message CreateAddressBookTagRequest {
  optional 6 subaccount_id = 1;
  optional 9 name = 2;
  optional 9 color = 3;
}
message CreateAddressBookTagResponse {
  optional .auth.v1.AddressBookTag tag = 1;
}
message UpdateAddressBookTagRequest {
  optional 6 tag_id = 1;
  optional 9 name = 2;
  optional 9 color = 3;
}
message UpdateAddressBookTagResponse {
  optional .auth.v1.AddressBookTag tag = 1;
}
message DeleteAddressBookTagRequest {
  optional 6 tag_id = 1;
}
message DeleteAddressBookTagResponse {
}
message ListTransferCounterpartiesRequest {
  optional 6 subaccount_id = 1;
  optional .auth.v1.TransferCounterpartyDirection direction = 2;
  optional .auth.v1.AddressBookEntryKind kind = 3;
  optional 13 limit = 5;
}
message ListTransferCounterpartiesResponse {
  repeated .auth.v1.TransferCounterparty counterparties = 1;
  optional 8 truncated = 2;
}
message ListTransferDestinationsRequest {
  optional 6 subaccount_id = 1;
  optional .auth.v1.AddressBookEntryKind kind = 2;
  optional 13 limit = 3;
  optional 9 page_token = 4;
}
message ListTransferDestinationsResponse {
  repeated .auth.v1.TransferDestination destinations = 1;
  optional 9 next_page_token = 2;
}
message ListInternalTransferWhitelistEntriesRequest {
  optional 6 subaccount_id = 1;
  optional 13 limit = 2;
  optional 9 page_token = 3;
}
message ListInternalTransferWhitelistEntriesResponse {
  repeated .auth.v1.InternalTransferWhitelistEntry entries = 1;
  optional 9 next_page_token = 2;
}
message GetWithdrawWhitelistViewRequest {
  optional 6 subaccount_id = 1;
}
message GetWithdrawWhitelistViewResponse {
  optional .auth.v1.WithdrawWhitelistView view = 1;
}
message GetAddressBookViewRequest {
  optional 6 subaccount_id = 1;
  optional 13 limit = 6;
  optional 4 minimum_view_revision = 7;
}
message GetAddressBookViewResponse {
  repeated .auth.v1.AddressBook books = 1;
  optional .auth.v1.AddressBookEntriesView entries = 2;
  optional .auth.v1.AddressBookRecentDestinationsView recent_destinations = 3;
  repeated .auth.v1.AddressBookTagSummary tags = 4;
  optional .auth.v1.WithdrawWhitelistView withdraw_whitelist = 5;
  optional 8 recent_destinations_truncated = 6;
  optional 4 view_revision = 7;
}
message AddressBookViewInvalidated {
  optional .auth.v1.AccountScopeRef scope = 1;
  optional .google.protobuf.Timestamp invalidated_at = 2;
  optional 4 view_revision = 3;
}
service AddressBookService {
  rpc ListAddressBooks(.auth.v1.ListAddressBooksRequest) returns (.auth.v1.ListAddressBooksResponse);
  rpc ListAddressBookEntries(.auth.v1.ListAddressBookEntriesRequest) returns (.auth.v1.ListAddressBookEntriesResponse);
  rpc CreateAddressBookEntry(.auth.v1.CreateAddressBookEntryRequest) returns (.auth.v1.CreateAddressBookEntryResponse);
  rpc UpdateAddressBookEntry(.auth.v1.UpdateAddressBookEntryRequest) returns (.auth.v1.UpdateAddressBookEntryResponse);
  rpc DeleteAddressBookEntry(.auth.v1.DeleteAddressBookEntryRequest) returns (.auth.v1.DeleteAddressBookEntryResponse);
  rpc CopyAddressBookEntry(.auth.v1.CopyAddressBookEntryRequest) returns (.auth.v1.CopyAddressBookEntryResponse);
  rpc CreateAddressBookTag(.auth.v1.CreateAddressBookTagRequest) returns (.auth.v1.CreateAddressBookTagResponse);
  rpc UpdateAddressBookTag(.auth.v1.UpdateAddressBookTagRequest) returns (.auth.v1.UpdateAddressBookTagResponse);
  rpc DeleteAddressBookTag(.auth.v1.DeleteAddressBookTagRequest) returns (.auth.v1.DeleteAddressBookTagResponse);
  rpc ListTransferCounterparties(.auth.v1.ListTransferCounterpartiesRequest) returns (.auth.v1.ListTransferCounterpartiesResponse);
  rpc ListTransferDestinations(.auth.v1.ListTransferDestinationsRequest) returns (.auth.v1.ListTransferDestinationsResponse);
  rpc ListInternalTransferWhitelistEntries(.auth.v1.ListInternalTransferWhitelistEntriesRequest) returns (.auth.v1.ListInternalTransferWhitelistEntriesResponse);
  rpc GetWithdrawWhitelistView(.auth.v1.GetWithdrawWhitelistViewRequest) returns (.auth.v1.GetWithdrawWhitelistViewResponse);
  rpc GetAddressBookView(.auth.v1.GetAddressBookViewRequest) returns (.auth.v1.GetAddressBookViewResponse);
}
```


## `auth_v1_api_keys`

```
// auth/v1/api_keys.proto  package=auth.v1
enum ApiKeyStatus {
  API_KEY_STATUS_UNSPECIFIED = 0;
  ACTIVE = 1;
  REVOKED = 2;
  DISABLED = 3;
}
message ApiKey {
  optional 9 key_id = 2;
  optional 9 label = 3;
  optional 9 icon = 9;
  optional 9 color = 10;
  repeated 9 ip_whitelist = 4;
  optional .auth.v1.ApiKeyStatus status = 6;
  optional 6 subaccount_id = 7;
  optional 6 policy_id = 8;
  optional .google.protobuf.Timestamp created_at = 20;
  optional .google.protobuf.Timestamp last_used_at = 21;
  optional 12 public_key_ed25519 = 22;
  optional .google.protobuf.Timestamp expires_at = 23;
  optional 9 created_by_actor = 24;
  optional .google.protobuf.Timestamp updated_at = 25;
  optional 4 revision = 26;
}
message CreateApiKeyRequest {
  optional 9 label = 1;
  optional 6 subaccount_id = 3;
  optional 9 icon = 6;
  optional 9 color = 7;
  repeated 9 ip_whitelist = 4;
  optional 12 public_key_ed25519 = 5;
}
message CreateApiKeyResponse {
  optional .auth.v1.ApiKey api_key = 1;
}
message ListApiKeysRequest {
  optional 6 subaccount_id = 1;
}
message ListApiKeysResponse {
  repeated .auth.v1.ApiKey api_keys = 1;
}
message DeleteApiKeyRequest {
  optional 9 key_id = 1;
}
message DeleteApiKeyResponse {
}
message GetApiKeyRequest {
  optional 9 key_id = 1;
}
message GetApiKeyResponse {
  optional .auth.v1.ApiKey api_key = 1;
}
message ApiKeyUpdateSpec {
  optional 9 label = 1;
  optional 9 icon = 2;
  optional 9 color = 3;
  optional .auth.v1.ApiKeyStatus status = 4;
  repeated 9 ip_whitelist = 5;
  optional .google.protobuf.Timestamp expires_at = 6;
}
message UpdateApiKeyRequest {
  optional 9 key_id = 1;
  optional .auth.v1.ApiKeyUpdateSpec api_key = 2;
  optional .google.protobuf.FieldMask update_mask = 3;
  optional 4 expected_revision = 4;
}
message UpdateApiKeyResponse {
  optional .auth.v1.ApiKey api_key = 1;
}
service ApiKeyService {
  rpc CreateApiKey(.auth.v1.CreateApiKeyRequest) returns (.auth.v1.CreateApiKeyResponse);
  rpc ListApiKeys(.auth.v1.ListApiKeysRequest) returns (.auth.v1.ListApiKeysResponse);
  rpc GetApiKey(.auth.v1.GetApiKeyRequest) returns (.auth.v1.GetApiKeyResponse);
  rpc DeleteApiKey(.auth.v1.DeleteApiKeyRequest) returns (.auth.v1.DeleteApiKeyResponse);
  rpc UpdateApiKey(.auth.v1.UpdateApiKeyRequest) returns (.auth.v1.UpdateApiKeyResponse);
}
```


## `auth_v1_auth`

```
// auth/v1/auth.proto  package=auth.v1
enum WalletChallengePurpose {
  WALLET_PROOF_UNSPECIFIED = 0;
  LOGIN = 1;
}
enum AuthErrorCode {
  AUTH_UNSPECIFIED = 0;
  AUTH_USERNAME_INVALID = 1;
  AUTH_USERNAME_TAKEN = 2;
  AUTH_USERNAME_COOLDOWN = 3;
  AUTH_USERNAME_FEATURE_LOCKED = 4;
  AUTH_USERNAME_RESERVED = 5;
  AUTH_INVALID_REQUEST = 6;
  AUTH_AUTHENTICATION_REQUIRED = 7;
  AUTH_SESSION_KIND_NOT_ALLOWED = 8;
  AUTH_WALLET_LOGIN_FAILED = 9;
  AUTH_RESOURCE_NOT_FOUND = 10;
  AUTH_SUBACCOUNT_ACCESS_DENIED = 11;
  AUTH_API_KEY_ACCESS_DENIED = 12;
  AUTH_API_KEY_INVALID_STATUS_TRANSITION = 14;
  AUTH_POLICY_INVALID = 15;
  AUTH_SMART_ACCOUNT_ALREADY_LINKED = 16;
  AUTH_INVITE_ACCESS_DENIED = 17;
  AUTH_INVITE_INVALID_STATE = 18;
  AUTH_MFA_DISABLED = 19;
  AUTH_MFA_NOT_ENROLLED = 20;
  AUTH_MFA_SESSION_INVALID = 21;
  AUTH_MFA_CHALLENGE_NOT_FOUND = 22;
  AUTH_MFA_CHALLENGE_INVALID = 23;
  AUTH_MFA_CHALLENGE_LOCKED = 24;
  AUTH_MFA_OTP_INVALID = 25;
  AUTH_MFA_RECOVERY_INVALID = 26;
  AUTH_MFA_PASSKEY_NOT_AVAILABLE = 27;
  AUTH_MFA_PASSKEY_CREDENTIAL_INVALID = 28;
  AUTH_MFA_PASSKEY_VERIFY_FAILED = 29;
  AUTH_MFA_ENROLLMENT_BINDING_INVALID = 30;
  AUTH_STEP_UP_REQUIRED = 31;
  AUTH_STEP_UP_PROOF_UNAVAILABLE = 32;
  AUTH_STEP_UP_ALREADY_CLAIMED = 33;
  AUTH_POLICY_IN_USE = 34;
  AUTH_POLICY_LOCKED = 35;
  AUTH_POLICY_SCOPE_MISMATCH = 36;
  AUTH_REVISION_CONFLICT = 37;
  AUTH_MFA_ELEVATION_REQUIRED = 38;
  AUTH_MFA_LAST_FACTOR_REQUIRED = 39;
  AUTH_INTERNAL_ERROR = 40;
  AUTH_TERMS_NOT_ACCEPTED = 41;
  AUTH_SOCIAL_VERIFICATION_EXPIRED = 42;
  AUTH_SOCIAL_VERIFICATION_INVALID_STATE = 43;
  AUTH_SUBACCOUNT_CHALLENGE_INVALID = 44;
  AUTH_SOCIAL_ACCOUNT_ALREADY_LINKED = 45;
}
message CreateWalletChallengeRequest {
  optional 9 smart_account_address = 1;
  optional 9 signer_address = 2;
  optional 9 uri = 3;
  optional .auth.v1.WalletChallengePurpose purpose = 4;
}
message CreateWalletChallengeResponse {
  optional 9 message = 1;
  optional .google.protobuf.Timestamp expires_at = 2;
}
message LoginWithWalletRequest {
  optional 9 smart_account_address = 1;
  optional 9 signature = 3;
  optional 9 user_agent = 4;
  optional 9 ip = 5;
  optional 9 wallet_provider = 7;
  optional 9 message = 8;
}
message LoginWithWalletResponse {
  optional 9 access_token = 1;
  optional .google.protobuf.Timestamp expires_at = 2;
  optional 6 account_id = 10;
  optional 9 username = 13;
  optional .auth.v1.SessionInfo session = 20;
}
message MeRequest {
}
message MeResponse {
  optional 6 account_id = 1;
  optional 9 api_key_id = 10;
  optional 9 username = 11;
  optional 9 root_smart_account_address = 12;
  optional .auth.v1.SessionInfo session = 20;
}
message AuthErrorDetail {
  optional .auth.v1.AuthErrorCode code = 1;
  optional 9 message = 2;
}
message AcceptTermsRequest {
}
message AcceptTermsResponse {
}
service AuthService {
  rpc CreateWalletChallenge(.auth.v1.CreateWalletChallengeRequest) returns (.auth.v1.CreateWalletChallengeResponse);
  rpc LoginWithWallet(.auth.v1.LoginWithWalletRequest) returns (.auth.v1.LoginWithWalletResponse);
  rpc AcceptTerms(.auth.v1.AcceptTermsRequest) returns (.auth.v1.AcceptTermsResponse);
  rpc Me(.auth.v1.MeRequest) returns (.auth.v1.MeResponse);
}
```


## `auth_v1_mfa`

```
// auth/v1/mfa.proto  package=auth.v1
enum SessionLevel {
  SESSION_LEVEL_UNSPECIFIED = 0;
  PRIMARY_AUTHENTICATED = 1;
  MFA_ELEVATED = 2;
  FRESH_STEP_UP = 3;
}
enum MFAFactorType {
  MFA_FACTOR_TYPE_UNSPECIFIED = 0;
  MFA_FACTOR_TYPE_TOTP = 1;
  MFA_FACTOR_TYPE_PASSKEY = 2;
  MFA_FACTOR_TYPE_RECOVERY_CODE = 3;
}
enum MFAChallengePurpose {
  MFA_CHALLENGE_PURPOSE_UNSPECIFIED = 0;
  MFA_CHALLENGE_PURPOSE_SESSION_ELEVATION = 1;
  MFA_CHALLENGE_PURPOSE_FRESH_STEP_UP = 2;
}
message SessionInfo {
  optional 9 session_id = 1;
  optional .auth.v1.SessionLevel session_level = 2;
  repeated 9 authentication_methods = 3;
  optional .google.protobuf.Timestamp auth_time = 4;
}
message MFAFactor {
  optional 9 factor_id = 1;
  optional .auth.v1.MFAFactorType factor_type = 2;
  optional 9 label = 3;
  optional .google.protobuf.Timestamp created_at = 4;
  optional .google.protobuf.Timestamp last_used_at = 5;
}
message ListMFAFactorsRequest {
}
message ListMFAFactorsResponse {
  repeated .auth.v1.MFAFactor factors = 1;
  optional 8 has_recovery_codes = 2;
}
message BeginTOTPEnrollmentRequest {
  optional 9 label = 1;
}
message BeginTOTPEnrollmentResponse {
  optional 9 enrollment_id = 1;
  optional 9 secret = 2;
  optional 9 otpauth_uri = 3;
  optional .google.protobuf.Timestamp expires_at = 4;
}
message FinishTOTPEnrollmentRequest {
  optional 9 enrollment_id = 1;
  optional 9 code = 2;
}
message FinishTOTPEnrollmentResponse {
  optional .auth.v1.MFAFactor factor = 1;
  repeated 9 recovery_codes = 2;
  optional .auth.v1.SessionInfo session = 3;
  optional 9 access_token = 4;
  optional .google.protobuf.Timestamp access_token_expires_at = 5;
}
message BeginPasskeyEnrollmentRequest {
  optional 9 label = 1;
}
message BeginPasskeyEnrollmentResponse {
  optional 9 enrollment_id = 1;
  optional .google.protobuf.Struct public_key = 2;
  optional .google.protobuf.Timestamp expires_at = 3;
}
message FinishPasskeyEnrollmentRequest {
  optional 9 enrollment_id = 1;
  optional .google.protobuf.Struct credential = 2;
}
message FinishPasskeyEnrollmentResponse {
  optional .auth.v1.MFAFactor factor = 1;
  repeated 9 recovery_codes = 2;
  optional .auth.v1.SessionInfo session = 3;
  optional 9 access_token = 4;
  optional .google.protobuf.Timestamp access_token_expires_at = 5;
}
message BeginMFAChallengeRequest {
  optional .auth.v1.MFAChallengePurpose purpose = 1;
}
message BeginMFAChallengeResponse {
  optional 9 challenge_id = 1;
  repeated .auth.v1.MFAFactorType allowed_factor_types = 2;
  optional .google.protobuf.Struct public_key = 3;
  optional .google.protobuf.Timestamp expires_at = 4;
}
message VerifyTOTPChallengeRequest {
  optional 9 challenge_id = 1;
  optional 9 code = 2;
}
message FinishPasskeyChallengeRequest {
  optional 9 challenge_id = 1;
  optional .google.protobuf.Struct credential = 2;
}
message VerifyRecoveryCodeChallengeRequest {
  optional 9 challenge_id = 1;
  optional 9 recovery_code = 2;
}
message CompleteMFAChallengeResponse {
  optional .auth.v1.SessionInfo session = 1;
  optional 9 access_token = 2;
  optional .google.protobuf.Timestamp access_token_expires_at = 3;
  optional 9 step_up_token = 4;
  optional .google.protobuf.Timestamp step_up_expires_at = 5;
}
message ClaimFreshStepUpRequest {
  optional 9 request_id = 1;
  optional 9 action_type = 2;
  optional 9 subject = 3;
}
message ClaimFreshStepUpResponse {
  optional 9 step_up_id = 1;
  optional 9 claim_nonce = 2;
  optional .google.protobuf.Timestamp claim_expires_at = 3;
}
message ConsumeFreshStepUpRequest {
  optional 9 step_up_id = 1;
  optional 9 request_id = 2;
  optional 9 action_type = 3;
  optional 9 subject = 4;
  optional 9 claim_nonce = 5;
}
message ConsumeFreshStepUpResponse {
}
message ReleaseFreshStepUpRequest {
  optional 9 step_up_id = 1;
  optional 9 request_id = 2;
  optional 9 action_type = 3;
  optional 9 subject = 4;
  optional 9 claim_nonce = 5;
  optional 9 reason = 6;
}
message ReleaseFreshStepUpResponse {
}
message UpdateMFAFactorRequest {
  optional 9 factor_id = 1;
  optional 9 label = 2;
}
message UpdateMFAFactorResponse {
  optional .auth.v1.MFAFactor factor = 1;
}
message DeleteMFAFactorRequest {
  optional 9 factor_id = 1;
}
message DeleteMFAFactorResponse {
}
message RegenerateRecoveryCodesRequest {
}
message RegenerateRecoveryCodesResponse {
  repeated 9 recovery_codes = 1;
}
service MFAService {
  rpc ListMFAFactors(.auth.v1.ListMFAFactorsRequest) returns (.auth.v1.ListMFAFactorsResponse);
  rpc BeginTOTPEnrollment(.auth.v1.BeginTOTPEnrollmentRequest) returns (.auth.v1.BeginTOTPEnrollmentResponse);
  rpc FinishTOTPEnrollment(.auth.v1.FinishTOTPEnrollmentRequest) returns (.auth.v1.FinishTOTPEnrollmentResponse);
  rpc BeginPasskeyEnrollment(.auth.v1.BeginPasskeyEnrollmentRequest) returns (.auth.v1.BeginPasskeyEnrollmentResponse);
  rpc FinishPasskeyEnrollment(.auth.v1.FinishPasskeyEnrollmentRequest) returns (.auth.v1.FinishPasskeyEnrollmentResponse);
  rpc BeginMFAChallenge(.auth.v1.BeginMFAChallengeRequest) returns (.auth.v1.BeginMFAChallengeResponse);
  rpc VerifyTOTPChallenge(.auth.v1.VerifyTOTPChallengeRequest) returns (.auth.v1.CompleteMFAChallengeResponse);
  rpc FinishPasskeyChallenge(.auth.v1.FinishPasskeyChallengeRequest) returns (.auth.v1.CompleteMFAChallengeResponse);
  rpc VerifyRecoveryCodeChallenge(.auth.v1.VerifyRecoveryCodeChallengeRequest) returns (.auth.v1.CompleteMFAChallengeResponse);
  rpc UpdateMFAFactor(.auth.v1.UpdateMFAFactorRequest) returns (.auth.v1.UpdateMFAFactorResponse);
  rpc DeleteMFAFactor(.auth.v1.DeleteMFAFactorRequest) returns (.auth.v1.DeleteMFAFactorResponse);
  rpc RegenerateRecoveryCodes(.auth.v1.RegenerateRecoveryCodesRequest) returns (.auth.v1.RegenerateRecoveryCodesResponse);
  rpc ClaimFreshStepUp(.auth.v1.ClaimFreshStepUpRequest) returns (.auth.v1.ClaimFreshStepUpResponse);
  rpc ConsumeFreshStepUp(.auth.v1.ConsumeFreshStepUpRequest) returns (.auth.v1.ConsumeFreshStepUpResponse);
  rpc ReleaseFreshStepUp(.auth.v1.ReleaseFreshStepUpRequest) returns (.auth.v1.ReleaseFreshStepUpResponse);
}
```


## `auth_v1_policies`

```
// auth/v1/policies.proto  package=auth.v1
enum PolicyAction {
  UNSPECIFIED = 0;
  TRADE_SPOT = 1;
  INTERNAL_TRANSFER = 3;
  EXTERNAL_WITHDRAW = 4;
  READ_BALANCES = 5;
  READ_SPOT = 6;
  READ_INTERNAL_TRANSFERS = 8;
  READ_ADDRESS_BOOK = 11;
  MANAGE_ADDRESS_BOOK = 12;
}
message MarketScope {
}
message SpotMarketSelector {
  optional 13 symbol_id = 1;
}
message SpotMarketRule {
  optional 13 symbol_id = 1;
}
message SubaccountPolicyView {
  optional 6 id = 1;
  optional 9 name = 2;
  optional 9 description = 3;
  repeated .auth.v1.SpotMarketRule spot_markets = 4;
  optional .auth.v1.MarketScope.Value spot_market_scope = 6;
  repeated .auth.v1.PolicyAction actions = 8;
  optional 8 is_template = 10;
  optional 6 source_template_id = 11;
  optional 4 max_order_notional = 13;
  optional 13 max_open_orders = 14;
  optional 8 trading_halted = 23;
  optional 8 locked = 27;
  optional .google.protobuf.Timestamp review_at = 28;
  optional .google.protobuf.Timestamp expires_at = 29;
  optional .google.protobuf.Timestamp created_at = 20;
  optional .google.protobuf.Timestamp updated_at = 21;
  optional 4 revision = 30;
}
message ListSubaccountPoliciesRequest {
  optional 6 subaccount_id = 1;
}
message ListSubaccountPoliciesResponse {
  repeated .auth.v1.SubaccountPolicyView policies = 1;
}
message GetSubaccountPolicyRequest {
  optional 6 policy_id = 1;
  optional 6 subaccount_id = 2;
}
message GetSubaccountPolicyResponse {
  optional .auth.v1.SubaccountPolicyView policy = 1;
}
message SubaccountPolicySpec {
  optional 9 name = 1;
  optional 9 description = 2;
  repeated .auth.v1.SpotMarketSelector spot_markets = 3;
  optional .auth.v1.MarketScope.Value spot_market_scope = 5;
  repeated .auth.v1.PolicyAction actions = 7;
  optional 4 max_order_notional = 13;
  optional 13 max_open_orders = 14;
  optional 8 trading_halted = 21;
  optional 8 locked = 25;
  optional .google.protobuf.Timestamp review_at = 26;
  optional .google.protobuf.Timestamp expires_at = 27;
}
message CreateSubaccountPolicyRequest {
  optional .auth.v1.SubaccountPolicySpec policy = 1;
  optional 6 subaccount_id = 2;
}
message CreateSubaccountPolicyResponse {
  optional .auth.v1.SubaccountPolicyView policy = 1;
}
message UpdateSubaccountPolicyRequest {
  optional 6 policy_id = 1;
  optional .auth.v1.SubaccountPolicySpec policy = 2;
  optional .google.protobuf.FieldMask update_mask = 3;
  optional 4 expected_revision = 4;
}
message UpdateSubaccountPolicyResponse {
  optional .auth.v1.SubaccountPolicyView policy = 1;
}
message DeleteSubaccountPolicyRequest {
  optional 6 policy_id = 1;
}
message DeleteSubaccountPolicyResponse {
}
message SetSubaccountPolicyRequest {
  optional 6 subaccount_id = 1;
  optional 6 policy_id = 2;
}
message SetSubaccountPolicyResponse {
}
message ApiPolicyView {
  optional 6 id = 1;
  optional 9 name = 2;
  optional 9 description = 3;
  repeated .auth.v1.SpotMarketRule spot_markets = 4;
  repeated .auth.v1.PolicyAction actions = 6;
  optional .auth.v1.MarketScope.Value spot_market_scope = 7;
  optional 8 is_template = 19;
  optional 6 source_template_id = 20;
  optional .google.protobuf.Timestamp created_at = 21;
  optional .google.protobuf.Timestamp updated_at = 22;
  optional 4 revision = 23;
}
message ListApiPoliciesRequest {
  optional 9 key_id = 1;
}
message ListApiPoliciesResponse {
  repeated .auth.v1.ApiPolicyView policies = 1;
}
message GetApiPolicyRequest {
  optional 6 policy_id = 1;
  optional 9 key_id = 2;
}
message GetApiPolicyResponse {
  optional .auth.v1.ApiPolicyView policy = 1;
}
message ApiPolicySpec {
  optional 9 name = 1;
  optional 9 description = 2;
  repeated .auth.v1.SpotMarketSelector spot_markets = 3;
  optional .auth.v1.MarketScope.Value spot_market_scope = 5;
  repeated .auth.v1.PolicyAction actions = 7;
  optional 8 is_template = 19;
}
message CreateApiPolicyRequest {
  optional .auth.v1.ApiPolicySpec policy = 1;
  optional 9 assign_to_key_id = 2;
}
message CreateApiPolicyResponse {
  optional .auth.v1.ApiPolicyView policy = 1;
}
message UpdateApiPolicyRequest {
  optional 6 policy_id = 1;
  optional .auth.v1.ApiPolicySpec policy = 2;
  optional .google.protobuf.FieldMask update_mask = 3;
  optional 4 expected_revision = 4;
}
message UpdateApiPolicyResponse {
  optional .auth.v1.ApiPolicyView policy = 1;
}
message DeleteApiPolicyRequest {
  optional 6 policy_id = 1;
}
message DeleteApiPolicyResponse {
}
message SetApiKeyPolicyRequest {
  optional 9 key_id = 1;
  optional 6 policy_id = 2;
}
message SetApiKeyPolicyResponse {
}
service PolicyService {
  rpc ListSubaccountPolicies(.auth.v1.ListSubaccountPoliciesRequest) returns (.auth.v1.ListSubaccountPoliciesResponse);
  rpc GetSubaccountPolicy(.auth.v1.GetSubaccountPolicyRequest) returns (.auth.v1.GetSubaccountPolicyResponse);
  rpc CreateSubaccountPolicy(.auth.v1.CreateSubaccountPolicyRequest) returns (.auth.v1.CreateSubaccountPolicyResponse);
  rpc UpdateSubaccountPolicy(.auth.v1.UpdateSubaccountPolicyRequest) returns (.auth.v1.UpdateSubaccountPolicyResponse);
  rpc DeleteSubaccountPolicy(.auth.v1.DeleteSubaccountPolicyRequest) returns (.auth.v1.DeleteSubaccountPolicyResponse);
  rpc SetSubaccountPolicy(.auth.v1.SetSubaccountPolicyRequest) returns (.auth.v1.SetSubaccountPolicyResponse);
  rpc ListApiPolicies(.auth.v1.ListApiPoliciesRequest) returns (.auth.v1.ListApiPoliciesResponse);
  rpc GetApiPolicy(.auth.v1.GetApiPolicyRequest) returns (.auth.v1.GetApiPolicyResponse);
  rpc CreateApiPolicy(.auth.v1.CreateApiPolicyRequest) returns (.auth.v1.CreateApiPolicyResponse);
  rpc UpdateApiPolicy(.auth.v1.UpdateApiPolicyRequest) returns (.auth.v1.UpdateApiPolicyResponse);
  rpc DeleteApiPolicy(.auth.v1.DeleteApiPolicyRequest) returns (.auth.v1.DeleteApiPolicyResponse);
  rpc SetApiKeyPolicy(.auth.v1.SetApiKeyPolicyRequest) returns (.auth.v1.SetApiKeyPolicyResponse);
}
```


## `auth_v1_profile`

```
// auth/v1/profile.proto  package=auth.v1
enum ProfileErrorCode {
  PROFILE_UNSPECIFIED = 0;
  PROFILE_INVALID_FIELD = 1;
  PROFILE_FIELD_TOO_LONG = 2;
  PROFILE_URL_INVALID = 3;
  PROFILE_URL_SCHEME_INVALID = 4;
}
message AccountIdentity {
  optional 6 account_id = 1;
  optional 9 username = 2;
  optional 9 avatar_url = 3;
  optional 9 root_smart_account_address = 4;
}
message UserProfile {
  optional 9 username = 1;
  optional 9 bio = 2;
  optional 9 website = 3;
  optional 9 twitter = 4;
  optional 8 twitter_verified = 8;
  optional 9 discord = 9;
  optional 8 discord_verified = 10;
  optional 9 avatar_url = 5;
  optional .google.protobuf.Timestamp created_at = 12;
  optional .google.protobuf.Timestamp next_username_change_at = 6;
  optional 5 vip_tier = 7;
  optional 8 username_unlocked = 11;
  optional 8 current_terms_accepted = 13;
}
message UserProfilePatch {
  optional 9 username = 1;
  optional 9 bio = 2;
  optional 9 website = 3;
  optional 9 twitter = 4;
  optional 9 avatar_url = 5;
}
message GetProfileRequest {
}
message ProfileErrorDetail {
  optional .auth.v1.ProfileErrorCode code = 1;
  optional 9 field = 2;
  optional 9 message = 3;
}
message UsernameHistoryEntry {
  optional 9 username = 1;
  optional .google.protobuf.Timestamp set_at = 2;
}
message GetUsernameHistoryRequest {
}
message GetUsernameHistoryResponse {
  repeated .auth.v1.UsernameHistoryEntry history = 1;
}
message GenerateUsernameOptionsRequest {
}
message GenerateUsernameOptionsResponse {
  repeated 9 usernames = 1;
  optional 9 offer_token = 2;
  optional .google.protobuf.Timestamp expires_at = 3;
}
message ClaimGeneratedUsernameRequest {
  optional 9 offer_token = 1;
  optional 13 option_index = 2;
}
service ProfileService {
  rpc GetProfile(.auth.v1.GetProfileRequest) returns (.auth.v1.UserProfile);
  rpc UpdateProfile(.auth.v1.UserProfilePatch) returns (.auth.v1.UserProfile);
  rpc GetUsernameHistory(.auth.v1.GetUsernameHistoryRequest) returns (.auth.v1.GetUsernameHistoryResponse);
  rpc GenerateUsernameOptions(.auth.v1.GenerateUsernameOptionsRequest) returns (.auth.v1.GenerateUsernameOptionsResponse);
  rpc ClaimGeneratedUsername(.auth.v1.ClaimGeneratedUsernameRequest) returns (.auth.v1.UserProfile);
}
```


## `auth_v1_resolve`

```
// auth/v1/resolve.proto  package=auth.v1
enum ResolveHint {
  RESOLVE_HINT_UNSPECIFIED = 0;
  USERNAME = 1;
  ID = 2;
  SMART_ACCOUNT = 3;
}
message ResolvedAccount {
  optional 9 smart_account_address = 1;
  optional .auth.v1.ResolvedAccount.Kind kind = 2;
  optional 9 root_username = 3;
  optional 9 subaccount_label = 4;
  optional 6 account_id = 5;
}
message ResolveAccountRequest {
  optional 9 query = 1;
  optional .auth.v1.ResolveHint hint = 2;
  optional 8 include_subaccounts = 3;
}
message ResolveAccountResponse {
  repeated .auth.v1.ResolvedAccount matches = 1;
}
service ResolveService {
  rpc ResolveAccount(.auth.v1.ResolveAccountRequest) returns (.auth.v1.ResolveAccountResponse);
}
```


## `auth_v1_social_verification`

```
// auth/v1/social_verification.proto  package=auth.v1
enum SocialProvider {
  PROVIDER_UNSPECIFIED = 0;
  TWITTER = 1;
  DISCORD = 2;
}
enum SocialVerificationStatus {
  STATUS_UNSPECIFIED = 0;
  STATUS_PENDING_USER_ACTION = 1;
  STATUS_QUEUED = 2;
  STATUS_IN_PROGRESS = 3;
  STATUS_VERIFIED = 4;
  STATUS_FAILED = 5;
  STATUS_EXPIRED = 6;
  STATUS_CANCELLED = 7;
}
enum SocialVerificationMethod {
  METHOD_UNSPECIFIED = 0;
  METHOD_PROFILE = 1;
  METHOD_CHANNEL = 2;
  METHOD_DM = 3;
}
message SocialVerification {
  optional 3 id = 12;
  optional .auth.v1.SocialProvider provider = 1;
  optional .auth.v1.SocialVerificationMethod method = 11;
  optional 9 handle = 2;
  optional 9 provider_user_id = 3;
  optional 9 challenge_code = 13;
  optional .auth.v1.SocialVerificationStatus status = 4;
  optional .google.protobuf.Timestamp requested_at = 5;
  optional .google.protobuf.Timestamp expires_at = 6;
  optional .google.protobuf.Timestamp verified_at = 7;
  optional 5 attempts = 9;
  optional 9 last_error = 10;
  optional .auth.v1.AuthErrorCode error_code = 16;
  optional .google.protobuf.Timestamp updated_at = 15;
}
message StartSocialVerificationRequest {
  optional .auth.v1.SocialProvider provider = 1;
  optional .auth.v1.SocialVerificationMethod method = 3;
  optional 9 handle = 2;
}
message StartSocialVerificationResponse {
  optional 9 challenge_code = 1;
  optional .google.protobuf.Timestamp expires_at = 2;
  optional .auth.v1.SocialVerification verification = 3;
}
message SocialVerificationReadyRequest {
  optional .auth.v1.SocialProvider provider = 1;
}
message SocialVerificationReadyResponse {
  optional .auth.v1.SocialVerification verification = 1;
}
message GetSocialVerificationRequest {
  optional .auth.v1.SocialProvider provider = 1;
}
message GetSocialVerificationResponse {
  optional .auth.v1.SocialVerification verification = 1;
}
service SocialVerificationService {
  rpc StartSocialVerification(.auth.v1.StartSocialVerificationRequest) returns (.auth.v1.StartSocialVerificationResponse);
  rpc SocialVerificationReady(.auth.v1.SocialVerificationReadyRequest) returns (.auth.v1.SocialVerificationReadyResponse);
  rpc GetSocialVerification(.auth.v1.GetSocialVerificationRequest) returns (.auth.v1.GetSocialVerificationResponse);
}
```


## `auth_v1_subaccounts`

```
// auth/v1/subaccounts.proto  package=auth.v1
enum SubaccountStatus {
  SUBACCOUNT_STATUS_UNSPECIFIED = 0;
  SUBACCOUNT_STATUS_ACTIVE = 1;
  SUBACCOUNT_STATUS_DISABLED = 2;
}
enum SubaccountRole {
  SUBACCOUNT_ROLE_UNSPECIFIED = 0;
  VIEWER = 1;
  TRADER = 2;
  LEVERAGED_TRADER = 3;
  TREASURY = 4;
  ADMIN = 5;
  OWNER = 6;
}
enum SubaccountPermission {
  SUBACCOUNT_PERMISSION_UNSPECIFIED = 0;
  SUBACCOUNT_PERMISSION_READ_SUBACCOUNT = 1;
  SUBACCOUNT_PERMISSION_UPDATE_SUBACCOUNT = 2;
  SUBACCOUNT_PERMISSION_READ_BALANCES = 3;
  SUBACCOUNT_PERMISSION_READ_SPOT = 4;
  SUBACCOUNT_PERMISSION_TRADE_SPOT = 5;
  SUBACCOUNT_PERMISSION_READ_INTERNAL_TRANSFERS = 6;
  SUBACCOUNT_PERMISSION_INTERNAL_TRANSFER = 7;
  SUBACCOUNT_PERMISSION_EXTERNAL_WITHDRAW = 8;
  SUBACCOUNT_PERMISSION_READ_ADDRESS_BOOK = 9;
  SUBACCOUNT_PERMISSION_MANAGE_ADDRESS_BOOK = 10;
  SUBACCOUNT_PERMISSION_READ_MEMBERS = 11;
  SUBACCOUNT_PERMISSION_MANAGE_MEMBERS = 12;
  SUBACCOUNT_PERMISSION_READ_INVITES = 13;
  SUBACCOUNT_PERMISSION_MANAGE_INVITES = 14;
  SUBACCOUNT_PERMISSION_READ_API_KEYS = 15;
  SUBACCOUNT_PERMISSION_MANAGE_API_KEYS = 16;
  SUBACCOUNT_PERMISSION_READ_SUBACCOUNT_POLICY = 17;
  SUBACCOUNT_PERMISSION_MANAGE_SUBACCOUNT_POLICY = 18;
  SUBACCOUNT_PERMISSION_READ_ACTIVITY = 19;
  SUBACCOUNT_PERMISSION_READ_ACTIVITY_SECURITY_DETAILS = 20;
  SUBACCOUNT_PERMISSION_MANAGE_MEMBER_MFA_REQUIREMENT = 21;
  SUBACCOUNT_PERMISSION_CREATE_DEPOSIT_ADDRESS = 22;
  SUBACCOUNT_PERMISSION_READ_DEPOSIT_ADDRESSES = 23;
  SUBACCOUNT_PERMISSION_READ_GUARD_SIGNER_STATUS = 24;
  SUBACCOUNT_PERMISSION_MANAGE_GUARD_SIGNER = 25;
}
enum SubaccountInviteStatus {
  SUBACCOUNT_INVITE_STATUS_UNSPECIFIED = 0;
  SUBACCOUNT_INVITE_STATUS_PENDING = 1;
  SUBACCOUNT_INVITE_STATUS_ACCEPTED = 2;
  SUBACCOUNT_INVITE_STATUS_DECLINED = 3;
  SUBACCOUNT_INVITE_STATUS_CANCELLED = 4;
}
enum SubaccountInviteDirection {
  DIRECTION_UNSPECIFIED = 0;
  INCOMING = 1;
  OUTGOING = 2;
}
enum SubaccountInviteAction {
  SUBACCOUNT_INVITE_ACTION_UNSPECIFIED = 0;
  SUBACCOUNT_INVITE_ACTION_ACCEPT = 1;
  SUBACCOUNT_INVITE_ACTION_DECLINE = 2;
  SUBACCOUNT_INVITE_ACTION_CANCEL = 3;
}
enum ActivityEntityKind {
  ACTIVITY_ENTITY_UNSPECIFIED = 0;
  ACTIVITY_ENTITY_ACCOUNT = 1;
  ACTIVITY_ENTITY_SESSION = 2;
  ACTIVITY_ENTITY_API_KEY = 3;
  ACTIVITY_ENTITY_SUBACCOUNT = 4;
  ACTIVITY_ENTITY_MEMBER = 5;
  ACTIVITY_ENTITY_POLICY = 6;
  ACTIVITY_ENTITY_INVITE = 7;
  ACTIVITY_ENTITY_SECURITY = 8;
  ACTIVITY_ENTITY_DESTINATION = 9;
}
enum ActivityEventAction {
  ACTIVITY_ACTION_UNSPECIFIED = 0;
  ACTIVITY_ACTION_CREATED = 1;
  ACTIVITY_ACTION_UPDATED = 2;
  ACTIVITY_ACTION_DELETED = 3;
  ACTIVITY_ACTION_ENABLED = 4;
  ACTIVITY_ACTION_DISABLED = 5;
  ACTIVITY_ACTION_REMOVED = 6;
  ACTIVITY_ACTION_ROLE_SET = 7;
  ACTIVITY_ACTION_RECEIVED = 8;
  ACTIVITY_ACTION_REPLIED = 9;
  ACTIVITY_ACTION_FAILED = 10;
  ACTIVITY_ACTION_REVOKED = 11;
  ACTIVITY_ACTION_BLOCKED = 12;
  ACTIVITY_ACTION_HOLD_PLACED = 13;
  ACTIVITY_ACTION_HOLD_RELEASED = 14;
}
enum ActivityEventSource {
  ACTIVITY_SOURCE_UNSPECIFIED = 0;
  ACTIVITY_SOURCE_WEB = 1;
  ACTIVITY_SOURCE_MOBILE = 2;
  ACTIVITY_SOURCE_API = 3;
}
message SubaccountPermissionDefinition {
  optional .auth.v1.SubaccountPermission permission = 1;
  optional 9 display_name = 2;
  optional 9 description = 3;
  optional .auth.v1.PolicyAction policy_action = 4;
}
message SubaccountRoleDefinition {
  optional .auth.v1.SubaccountRole role = 1;
  optional 9 display_name = 2;
  optional 9 description = 3;
  optional 8 assignable = 4;
  repeated .auth.v1.SubaccountPermission permissions = 5;
}
message ListSubaccountRolesRequest {
}
message ListSubaccountRolesResponse {
  repeated .auth.v1.SubaccountPermissionDefinition permissions = 1;
  repeated .auth.v1.SubaccountRoleDefinition roles = 2;
}
message GetEffectiveSubaccountPermissionsRequest {
  optional 6 subaccount_id = 1;
}
message GetEffectiveSubaccountPermissionsResponse {
  optional .auth.v1.SubaccountRole role = 1;
  repeated .auth.v1.SubaccountPermission permissions = 2;
  optional 6 subaccount_policy_id = 3;
}
message SubaccountRoleView {
  optional 6 subaccount_id = 1;
  optional .auth.v1.SubaccountRole role = 2;
}
message Subaccount {
  optional 6 id = 1;
  optional .auth.v1.SubaccountRole role = 2;
  optional 9 label = 3;
  optional 9 icon = 10;
  optional 9 color = 11;
  optional .auth.v1.SubaccountStatus status = 4;
  optional 9 smart_account_address = 5;
  optional 9 owner_username = 6;
  optional 9 owner_avatar_url = 7;
  optional 9 owner_root_smart_account_address = 8;
  optional 6 subaccount_policy_id = 9;
  optional 8 require_member_mfa = 12;
  optional 13 smart_account_salt_nonce = 13;
  optional .google.protobuf.Timestamp updated_at = 14;
  optional 4 revision = 15;
}
message ListSubaccountsRequest {
}
message ListSubaccountsResponse {
  repeated .auth.v1.Subaccount subaccounts = 1;
  optional 13 total_created = 2;
}
message CreateSubaccountChallengeRequest {
  optional 9 owner_address = 1;
  optional 9 uri = 2;
}
message CreateSubaccountChallengeResponse {
  optional 9 message = 1;
  optional 9 smart_account_address = 2;
  optional 13 smart_account_salt_nonce = 3;
  optional .google.protobuf.Timestamp expires_at = 4;
  optional 4 polyester_chain_id = 5;
}
message CreateSubaccountRequest {
  optional 9 label = 1;
  optional 9 icon = 7;
  optional 9 color = 8;
  optional 9 smart_account_address = 2;
  optional 9 message = 3;
  optional 9 signature = 4;
}
message CreateSubaccountResponse {
  optional 6 subaccount_id = 1;
  optional 13 total_created = 2;
  optional 13 smart_account_salt_nonce = 3;
  optional 4 revision = 4;
}
message SubaccountUpdateSpec {
  optional 9 label = 1;
  optional 9 icon = 2;
  optional 9 color = 3;
  optional .auth.v1.SubaccountStatus status = 4;
}
message UpdateSubaccountRequest {
  optional 6 subaccount_id = 1;
  optional .auth.v1.SubaccountUpdateSpec subaccount = 2;
  optional .google.protobuf.FieldMask update_mask = 3;
  optional 4 expected_revision = 4;
}
message UpdateSubaccountResponse {
  optional .auth.v1.Subaccount subaccount = 1;
}
message SetSubaccountMemberMFARequirementRequest {
  optional 6 subaccount_id = 1;
  optional 8 require_member_mfa = 2;
}
message SetSubaccountMemberMFARequirementResponse {
}
message SubaccountMemberView {
  optional 6 account_id = 1;
  optional .auth.v1.SubaccountRole role = 2;
  optional 9 username = 3;
  optional 9 smart_account_address = 4;
  optional 9 avatar_url = 5;
  optional 8 mfa_enrolled = 6;
}
message ListSubaccountMembersRequest {
  optional 6 subaccount_id = 1;
}
message ListSubaccountMembersResponse {
  repeated .auth.v1.SubaccountMemberView members = 1;
}
message RemoveSubaccountMemberRequest {
  optional 6 subaccount_id = 1;
  optional 6 grantee_account_id = 2;
}
message RemoveSubaccountMemberResponse {
}
message UpdateSubaccountMemberRoleRequest {
  optional 6 subaccount_id = 1;
  optional 6 grantee_account_id = 2;
  optional .auth.v1.SubaccountRole role = 3;
}
message UpdateSubaccountMemberRoleResponse {
}
message SubaccountInvite {
  optional 6 id = 1;
  optional 6 subaccount_id = 2;
  optional 6 grantee_account_id = 3;
  optional 6 inviter_account_id = 4;
  optional .auth.v1.SubaccountRole role = 5;
  optional .auth.v1.SubaccountInviteStatus status = 6;
  optional .google.protobuf.Timestamp created_at = 7;
  optional .google.protobuf.Timestamp responded_at = 8;
  optional 9 grantee_username = 9;
  optional 9 inviter_username = 10;
  optional 9 subaccount_label = 11;
  optional 9 inviter_root_smart_account_address = 12;
  optional 9 grantee_root_smart_account_address = 13;
  optional 8 require_member_mfa = 14;
}
message InviteSubaccountMemberRequest {
  optional 6 subaccount_id = 1;
  optional 6 grantee_account_id = 2;
  optional .auth.v1.SubaccountRole role = 3;
}
message InviteSubaccountMemberResponse {
  optional .auth.v1.SubaccountInvite invite = 1;
}
message ListSubaccountInvitesRequest {
  optional .auth.v1.SubaccountInviteDirection direction = 1;
}
message ListSubaccountInvitesResponse {
  repeated .auth.v1.SubaccountInvite invites = 1;
}
message RespondSubaccountInviteRequest {
  optional 6 invite_id = 1;
  optional .auth.v1.SubaccountInviteAction action = 2;
}
message RespondSubaccountInviteResponse {
  optional .auth.v1.SubaccountInvite invite = 1;
}
message GetSubaccountRequest {
  optional 6 subaccount_id = 1;
  optional 8 include_api_keys = 2;
  optional 8 include_members = 3;
  optional 8 include_invites = 4;
  optional 8 include_policy = 5;
  optional 8 include_balances = 6;
  optional .auth.v1.SubaccountInviteDirection invites_direction = 7;
}
message GetSubaccountResponse {
  optional .auth.v1.Subaccount subaccount = 1;
  repeated .auth.v1.ApiKey api_keys = 2;
  repeated .auth.v1.SubaccountMemberView members = 3;
  repeated .auth.v1.SubaccountInvite invites = 4;
  optional .auth.v1.SubaccountPolicyView policy = 5;
  optional .ledger.read.v1.GetBalancesResponse balances = 6;
}
message ActivityEvent {
  optional .google.protobuf.Timestamp created_at = 2;
  optional .auth.v1.ActivityEntityKind entity_kind = 3;
  optional .auth.v1.ActivityEventAction event_action = 4;
  optional .auth.v1.ActivityEventSource source = 5;
  optional 9 ip = 6;
  optional 9 user_agent = 7;
  optional 6 actor_account_id = 8;
  optional 9 payload_json = 9;
}
message ListSubaccountEventsRequest {
  optional 6 subaccount_id = 1;
  optional 13 limit = 2;
  optional 9 page_token = 4;
}
message ListSubaccountEventsResponse {
  repeated .auth.v1.ActivityEvent events = 1;
  optional 9 next_page_token = 3;
}
service SubaccountViewService {
  rpc GetSubaccount(.auth.v1.GetSubaccountRequest) returns (.auth.v1.GetSubaccountResponse);
  rpc ListSubaccountActivity(.auth.v1.ListSubaccountEventsRequest) returns (.auth.v1.ListSubaccountEventsResponse);
}
service SubaccountService {
  rpc ListSubaccounts(.auth.v1.ListSubaccountsRequest) returns (.auth.v1.ListSubaccountsResponse);
  rpc CreateSubaccountChallenge(.auth.v1.CreateSubaccountChallengeRequest) returns (.auth.v1.CreateSubaccountChallengeResponse);
  rpc CreateSubaccount(.auth.v1.CreateSubaccountRequest) returns (.auth.v1.CreateSubaccountResponse);
  rpc UpdateSubaccount(.auth.v1.UpdateSubaccountRequest) returns (.auth.v1.UpdateSubaccountResponse);
  rpc SetSubaccountMemberMFARequirement(.auth.v1.SetSubaccountMemberMFARequirementRequest) returns (.auth.v1.SetSubaccountMemberMFARequirementResponse);
  rpc ListSubaccountMembers(.auth.v1.ListSubaccountMembersRequest) returns (.auth.v1.ListSubaccountMembersResponse);
  rpc RemoveSubaccountMember(.auth.v1.RemoveSubaccountMemberRequest) returns (.auth.v1.RemoveSubaccountMemberResponse);
  rpc UpdateSubaccountMemberRole(.auth.v1.UpdateSubaccountMemberRoleRequest) returns (.auth.v1.UpdateSubaccountMemberRoleResponse);
  rpc InviteSubaccountMember(.auth.v1.InviteSubaccountMemberRequest) returns (.auth.v1.InviteSubaccountMemberResponse);
  rpc ListSubaccountInvites(.auth.v1.ListSubaccountInvitesRequest) returns (.auth.v1.ListSubaccountInvitesResponse);
  rpc RespondSubaccountInvite(.auth.v1.RespondSubaccountInviteRequest) returns (.auth.v1.RespondSubaccountInviteResponse);
}
service SubaccountRoleService {
  rpc ListSubaccountRoles(.auth.v1.ListSubaccountRolesRequest) returns (.auth.v1.ListSubaccountRolesResponse);
  rpc GetEffectiveSubaccountPermissions(.auth.v1.GetEffectiveSubaccountPermissionsRequest) returns (.auth.v1.GetEffectiveSubaccountPermissionsResponse);
}
```


## `chain_analytics_v1_analytics_read`

```
// chain/analytics/v1/analytics_read.proto  package=chain.analytics.v1
enum ChainAnalyticsRange {
  RANGE_UNSPECIFIED = 0;
  DAY_1 = 1;
  DAY_7 = 2;
  DAY_30 = 3;
  DAY_90 = 4;
  DAY_180 = 5;
  DAY_365 = 6;
}
message GetZippedAssetSupplyRequest {
  optional 13 zipped_asset_id = 1;
  optional .chain.analytics.v1.ChainAnalyticsRange range = 2;
  optional 9 bucket = 3;
  optional 7 start_ts_sec = 4;
  optional 7 end_ts_sec = 5;
}
message GetZippedAssetSupplyResponse {
  optional 13 zipped_asset_id = 1;
  optional .chain.analytics.v1.ChainAnalyticsRange range = 2;
  optional 9 bucket = 3;
  optional 7 start_ts_sec = 4;
  optional 7 end_ts_sec = 5;
  optional 13 points = 6;
  repeated 4 total_supply_q = 7;
}
message ZippedAssetSupplySeries {
  optional 13 zipped_asset_id = 1;
  repeated 4 total_supply_q = 2;
}
message GetZippedAssetSupplyGroupRequest {
  optional 9 group_id = 1;
  optional .chain.analytics.v1.ChainAnalyticsRange range = 2;
  optional 9 bucket = 3;
  optional 7 start_ts_sec = 4;
  optional 7 end_ts_sec = 5;
}
message GetZippedAssetSupplyGroupResponse {
  optional 9 group_id = 1;
  optional .chain.analytics.v1.ChainAnalyticsRange range = 2;
  optional 9 bucket = 3;
  optional 7 start_ts_sec = 4;
  optional 7 end_ts_sec = 5;
  optional 13 points = 6;
  repeated .chain.analytics.v1.ZippedAssetSupplySeries series = 7;
}
message GetUnifiedAssetBalancesRequest {
  optional 13 asset_id = 1;
  optional .chain.analytics.v1.ChainAnalyticsRange range = 2;
  optional 9 bucket = 3;
  optional 7 start_ts_sec = 4;
  optional 7 end_ts_sec = 5;
}
message GetUnifiedAssetBalancesResponse {
  optional 13 asset_id = 1;
  optional .chain.analytics.v1.ChainAnalyticsRange range = 2;
  optional 9 bucket = 3;
  optional 7 start_ts_sec = 4;
  optional 7 end_ts_sec = 5;
  optional 13 points = 6;
  repeated 4 total_balance_q = 7;
}
service ChainAnalyticsService {
  rpc GetZippedAssetSupply(.chain.analytics.v1.GetZippedAssetSupplyRequest) returns (.chain.analytics.v1.GetZippedAssetSupplyResponse);
  rpc GetZippedAssetSupplyGroup(.chain.analytics.v1.GetZippedAssetSupplyGroupRequest) returns (.chain.analytics.v1.GetZippedAssetSupplyGroupResponse);
  rpc GetUnifiedAssetBalances(.chain.analytics.v1.GetUnifiedAssetBalancesRequest) returns (.chain.analytics.v1.GetUnifiedAssetBalancesResponse);
}
```


## `chain_deposit_v1_deposit`

```
// chain/deposit/v1/deposit.proto  package=chain.deposit.v1
message DepositAddress {
  optional 13 chain_id = 1;
  optional 9 deposit_address = 2;
}
message CreateDepositAddressRequest {
  optional 6 subaccount_id = 1;
  optional 13 chain_id = 2;
}
message CreateDepositAddressResponse {
  optional .chain.deposit.v1.DepositAddress deposit_address = 1;
}
message ListDepositAddressesRequest {
  optional 6 subaccount_id = 1;
  optional 13 chain_id = 2;
}
message ListDepositAddressesResponse {
  repeated .chain.deposit.v1.DepositAddress deposit_addresses = 1;
}
service DepositAddressService {
  rpc CreateDepositAddress(.chain.deposit.v1.CreateDepositAddressRequest) returns (.chain.deposit.v1.CreateDepositAddressResponse);
  rpc ListDepositAddresses(.chain.deposit.v1.ListDepositAddressesRequest) returns (.chain.deposit.v1.ListDepositAddressesResponse);
}
```


## `chain_guard_v1_guard_signer`

```
// chain/guard/v1/guard_signer.proto  package=chain.guard.v1
enum ProtectedAction {
  PROTECTED_ACTION_UNSPECIFIED = 0;
  PROTECTED_ACTION_FUNDING_SET_EXTERNAL_WHITELIST_REQUIRED = 1;
  PROTECTED_ACTION_FUNDING_ADD_EXTERNAL_WHITELIST = 2;
  PROTECTED_ACTION_FUNDING_REMOVE_EXTERNAL_WHITELIST = 3;
  PROTECTED_ACTION_FUNDING_ADD_INTERNAL_WHITELIST = 4;
  PROTECTED_ACTION_FUNDING_REMOVE_INTERNAL_WHITELIST = 5;
  PROTECTED_ACTION_FUNDING_SET_INTERNAL_WHITELIST_REQUIRED = 6;
}
message GuardSignerStatus {
  optional 9 signer_address = 1;
  optional 9 onchain_signer_address = 2;
  optional 8 initialized = 3;
  optional 9 nonce = 4;
  optional 4 nonce_space = 5;
}
message GuardApproval {
  optional 4 nonce_space = 1;
  optional 4 deadline_unix = 2;
  optional 12 signature = 3;
}
message ExternalWhitelistArgs {
  optional 13 polychain_chain_id = 1;
  repeated 9 addresses = 2;
}
message InternalWhitelistArgs {
  repeated 9 addresses = 1;
}
message WhitelistRequirementArgs {
  optional 8 required = 1;
}
message ProtectedActionArgs {
  optional .chain.guard.v1.ExternalWhitelistArgs external_whitelist = 1;
  optional .chain.guard.v1.InternalWhitelistArgs internal_whitelist = 2;
  optional .chain.guard.v1.WhitelistRequirementArgs whitelist_requirement = 3;
}
message CreateGuardSignerWalletRequest {
  optional 6 subaccount_id = 1;
}
message CreateGuardSignerWalletResponse {
  optional 9 signer_address = 1;
}
message GetGuardSignerStatusRequest {
  optional 6 subaccount_id = 1;
}
message GetGuardSignerStatusResponse {
  optional .chain.guard.v1.GuardSignerStatus status = 1;
}
message SignProtectedActionRequest {
  optional 6 subaccount_id = 1;
  optional .chain.guard.v1.ProtectedAction action = 2;
  optional .chain.guard.v1.ProtectedActionArgs args = 3;
}
message SignProtectedActionResponse {
  optional .chain.guard.v1.GuardApproval approval = 1;
}
message BatchSignProtectedActionItem {
  optional .chain.guard.v1.ProtectedAction action = 1;
  optional .chain.guard.v1.ProtectedActionArgs args = 2;
}
message BatchSignProtectedActionsRequest {
  optional 6 subaccount_id = 1;
  repeated .chain.guard.v1.BatchSignProtectedActionItem actions = 2;
}
message BatchSignProtectedActionsResponse {
  repeated .chain.guard.v1.GuardApproval approvals = 1;
}
message RotateGuardSignerWalletRequest {
  optional 6 subaccount_id = 1;
}
message RotateGuardSignerWalletResponse {
  optional 9 new_signer_address = 1;
  optional .chain.guard.v1.GuardApproval approval = 2;
}
message ExportGuardSignerWalletRequest {
  optional 6 subaccount_id = 1;
}
message ExportGuardSignerWalletResponse {
  optional 9 private_key = 1;
}
service GuardSignerService {
  rpc CreateGuardSignerWallet(.chain.guard.v1.CreateGuardSignerWalletRequest) returns (.chain.guard.v1.CreateGuardSignerWalletResponse);
  rpc GetGuardSignerStatus(.chain.guard.v1.GetGuardSignerStatusRequest) returns (.chain.guard.v1.GetGuardSignerStatusResponse);
  rpc SignProtectedAction(.chain.guard.v1.SignProtectedActionRequest) returns (.chain.guard.v1.SignProtectedActionResponse);
  rpc BatchSignProtectedActions(.chain.guard.v1.BatchSignProtectedActionsRequest) returns (.chain.guard.v1.BatchSignProtectedActionsResponse);
  rpc RotateGuardSignerWallet(.chain.guard.v1.RotateGuardSignerWalletRequest) returns (.chain.guard.v1.RotateGuardSignerWalletResponse);
  rpc ExportGuardSignerWallet(.chain.guard.v1.ExportGuardSignerWalletRequest) returns (.chain.guard.v1.ExportGuardSignerWalletResponse);
}
```


## `chain_lifecycle_v1_lifecycle_read`

```
// chain/lifecycle/v1/lifecycle_read.proto  package=chain.lifecycle.v1
enum TxLookupKind {
  TX_UNSPECIFIED = 0;
  TX_SOURCE = 1;
  TX_ANY = 2;
}
enum ListScope {
  LIST_UNSPECIFIED = 0;
  LIST_ALL = 1;
  LIST_OPEN_ONLY = 2;
  LIST_TERMINAL_ONLY = 3;
}
enum Sort {
  SORT_UNSPECIFIED = 0;
  SORT_NEWEST = 1;
  SORT_OLDEST = 2;
}
enum ListOrderBy {
  ORDER_BY_UNSPECIFIED = 0;
  ORDER_BY_LAST_ACTIVITY = 1;
  ORDER_BY_STARTED_AT = 2;
}
enum FlowStep {
  FLOW_STEP_UNSPECIFIED = 0;
  FLOW_STEP_SOURCE = 1;
  FLOW_STEP_TRANSFER = 2;
  FLOW_STEP_REQUEST = 3;
  FLOW_STEP_VALIDATION = 4;
  FLOW_STEP_EXECUTION = 5;
  FLOW_STEP_BRIDGE_FULFILLMENT = 6;
  FLOW_STEP_DROPPED = 7;
  FLOW_STEP_FAILED = 8;
  FLOW_STEP_REFUNDED = 9;
  FLOW_STEP_FULFILLING = 10;
  FLOW_STEP_SETTLEMENT = 11;
}
enum FlowStepActivityKind {
  ACTIVITY_UNSPECIFIED = 0;
  ACTIVITY_MINTED = 1;
  ACTIVITY_FUNDING = 2;
  ACTIVITY_TRADING = 3;
}
enum FlowTimelineStatus {
  TIMELINE_STATUS_UNSPECIFIED = 0;
  TIMELINE_STATUS_COMPLETED = 1;
  TIMELINE_STATUS_CURRENT = 2;
  TIMELINE_STATUS_PLANNED = 3;
}
message GetFlowResponse {
  optional .chain.lifecycle.v1.FlowDetailView flow = 1;
}
message GetFlowByIdRequest {
  optional 9 flow_id = 1;
}
message ListFlowsByTxRequest {
  optional 9 tx_hash = 1;
  optional .chain.lifecycle.v1.TxLookupKind lookup_kind = 2;
  optional 13 limit = 3;
  optional 9 page_token = 4;
}
message ListFlowsRequest {
  optional 13 limit = 1;
  optional .chain.lifecycle.v1.Sort sort = 2;
  optional .chain.lifecycle.v1.FlowKind flow_kind = 3;
  optional .chain.lifecycle.v1.FlowState flow_state = 4;
  optional 9 tx_ref = 5;
  optional .chain.lifecycle.v1.ListScope scope = 6;
  optional 6 owner_account_id = 7;
  optional 9 smart_account_address = 8;
  repeated 13 polyester_chain_ids = 9;
  repeated 13 zipped_asset_ids = 10;
  repeated 13 unified_asset_ids = 11;
  optional 9 page_token = 12;
  optional .chain.lifecycle.v1.ListOrderBy order_by = 13;
}
message ListFlowsResponse {
  repeated .chain.lifecycle.v1.FlowSummaryView flows = 1;
  optional 9 next_page_token = 2;
}
message FlowTxMatchView {
  optional 9 flow_id = 1;
  optional .chain.lifecycle.v1.FlowKind flow_kind = 3;
  optional 9 source_tx_hash = 4;
  optional 9 latest_tx_ref = 5;
  optional 4 tx_occurrence_index = 6;
  optional .chain.lifecycle.v1.FlowDomain source_domain = 7;
  optional .chain.lifecycle.v1.FlowDomain destination_domain = 8;
  optional .chain.lifecycle.v1.FlowStep current_step = 9;
  optional 8 is_open = 10;
  optional 8 is_terminal = 11;
  optional .chain.lifecycle.v1.AssetIds asset_ids = 12;
  optional 13 polyester_chain_id = 13;
  optional .polyester.type.v1.U128 amount_e18 = 14;
  optional 9 source_address = 15;
  optional 9 destination_address = 16;
  optional .chain.lifecycle.v1.LifecycleReason lifecycle_reason = 17;
  optional 4 last_activity_at_unix_ms = 18;
  optional 6 owner_account_id = 19;
  optional 9 smart_account_address = 20;
  optional .chain.zipper.v1.ZipperReasonDetails zipper_reason = 21;
}
message ListFlowsByTxResponse {
  optional 9 tx_hash = 1;
  repeated .chain.lifecycle.v1.FlowTxMatchView matches = 2;
  optional 9 next_page_token = 3;
}
message FlowSummaryView {
  optional 6 owner_account_id = 1;
  optional 9 smart_account_address = 34;
  optional 9 flow_id = 33;
  optional .chain.lifecycle.v1.FlowKind flow_kind = 4;
  optional .chain.lifecycle.v1.FlowStep current_step = 6;
  optional .chain.lifecycle.v1.AssetIds asset_ids = 7;
  optional 13 polyester_chain_id = 8;
  optional .polyester.type.v1.U128 amount_e18 = 9;
  optional .chain.lifecycle.v1.RequestFee request_fee = 28;
  optional 9 source_tx_hash = 11;
  optional 4 tx_occurrence_index = 32;
  optional 9 source_address = 13;
  optional 9 destination_address = 14;
  optional 9 latest_tx_ref = 15;
  optional .chain.lifecycle.v1.FlowDomain source_domain = 29;
  optional .chain.lifecycle.v1.FlowDomain destination_domain = 30;
  optional .chain.lifecycle.v1.LifecycleSource latest_lifecycle_source = 16;
  optional .chain.lifecycle.v1.LifecycleReason lifecycle_reason = 17;
  optional .chain.zipper.v1.ZipperReasonDetails zipper_reason = 35;
  optional 4 started_at_unix_ms = 18;
  optional 4 updated_at_unix_ms = 19;
  optional 4 terminal_at_unix_ms = 20;
  optional 4 last_activity_at_unix_ms = 21;
  optional 8 is_open = 22;
  optional 8 is_terminal = 23;
  optional 13 current_step_sequence = 24;
  optional .chain.lifecycle.v1.FlowSummaryProgressView current_progress = 25;
  repeated .chain.lifecycle.v1.FlowTimelineItemView progress_timeline = 26;
  optional 4 estimated_completion_unix_ms = 27;
}
message FlowSummaryProgressView {
  optional 4 current_step_started_at_unix_ms = 1;
  optional 4 current_step_expected_duration_ms = 2;
  optional 13 current_confirmations = 5;
  optional 13 required_confirmations = 6;
  optional 13 approve_count = 7;
  optional 13 reject_count = 8;
  optional 13 validator_count = 9;
  optional 13 required_approvals = 10;
  optional 13 required_rejections = 11;
}
message FlowStepView {
  optional 13 sequence = 1;
  optional .chain.lifecycle.v1.FlowStep step = 3;
  optional .chain.lifecycle.v1.AssetIds asset_ids = 7;
  optional 13 polyester_chain_id = 8;
  optional .polyester.type.v1.U128 amount_e18 = 9;
  optional .chain.lifecycle.v1.RequestFee request_fee = 24;
  optional 9 milestone_tx_ref = 11;
  optional .chain.lifecycle.v1.LifecycleSource lifecycle_source = 12;
  optional .chain.lifecycle.v1.LifecycleReason lifecycle_reason = 13;
  optional .chain.zipper.v1.ZipperReasonDetails zipper_reason = 25;
  optional 13 current_confirmations = 14;
  optional 13 required_confirmations = 15;
  optional 13 approve_count = 16;
  optional 13 reject_count = 17;
  optional 13 validator_count = 18;
  optional 13 required_approvals = 22;
  optional 13 required_rejections = 23;
  optional 4 occurred_at_unix_ms = 19;
  optional 4 block_time_moving_average_ms = 20;
  repeated .chain.lifecycle.v1.FlowStepActivityView activities = 21;
}
message FlowStepActivityView {
  optional 13 sequence = 1;
  optional 9 tx_ref = 2;
  optional 4 occurred_at_unix_ms = 3;
  optional .chain.lifecycle.v1.LifecycleSource lifecycle_source = 4;
  optional .chain.lifecycle.v1.LifecycleReason lifecycle_reason = 5;
  optional .chain.zipper.v1.ZipperReasonDetails zipper_reason = 16;
  optional 13 current_confirmations = 6;
  optional 13 required_confirmations = 7;
  optional 13 approve_count = 8;
  optional 13 reject_count = 9;
  optional 13 validator_count = 10;
  optional .chain.lifecycle.v1.FlowStepActivityKind kind = 11;
  optional 13 required_approvals = 12;
  optional 13 required_rejections = 13;
  optional .polyester.type.v1.U128 amount_e18 = 14;
  optional 9 ledger_transfer_id = 15;
}
message FlowTimelineItemView {
  optional 13 sequence = 1;
  optional .chain.lifecycle.v1.FlowStep step = 2;
  optional .chain.lifecycle.v1.FlowTimelineStatus status = 3;
  optional 4 expected_duration_ms = 4;
}
message FlowDetailView {
  optional .chain.lifecycle.v1.FlowSummaryView summary = 1;
  repeated .chain.lifecycle.v1.FlowStepView observed_steps = 2;
  optional 8 from_live_state = 3;
}
service LifecycleReadService {
  rpc GetFlowById(.chain.lifecycle.v1.GetFlowByIdRequest) returns (.chain.lifecycle.v1.GetFlowResponse);
  rpc ListFlows(.chain.lifecycle.v1.ListFlowsRequest) returns (.chain.lifecycle.v1.ListFlowsResponse);
  rpc ListFlowsByTx(.chain.lifecycle.v1.ListFlowsByTxRequest) returns (.chain.lifecycle.v1.ListFlowsByTxResponse);
}
```


## `chain_lifecycle_v1_types`

```
// chain/lifecycle/v1/types.proto  package=chain.lifecycle.v1
enum RequestFeeStatus {
  REQUEST_FEE_STATUS_UNSPECIFIED = 0;
  REQUEST_FEE_STATUS_LOCKED = 1;
  REQUEST_FEE_STATUS_SETTLED = 2;
}
enum LifecycleReason {
  REASON_UNSPECIFIED = 0;
  ZIPPER_VALIDATION_REJECTED = 101;
  ZIPPER_EXECUTION_REJECTED = 102;
  ZIPPER_WITHDRAW_EXECUTION_FAILED = 103;
  ZIPPER_DEPOSIT_REFUND_FAILED = 104;
  LEDGER_MIRROR_REJECTED = 200;
  LEDGER_MIRROR_TRANSFER_EXCEEDS_CREDITS = 201;
  LEDGER_MIRROR_TRANSFER_EXISTS = 202;
  LEDGER_MIRROR_PENDING_TRANSFER_NOT_FOUND = 203;
  LEDGER_MIRROR_TRANSFER_ID_ALREADY_FAILED = 204;
  TRADING_WITHDRAW_POLICY_DENIED = 300;
  TRADING_WITHDRAW_CONTRACT_REVERTED = 301;
  TRADING_WITHDRAW_EXECUTION_FAILED = 302;
}
enum FlowKind {
  KIND_UNSPECIFIED = 0;
  KIND_DEPOSIT = 1;
  KIND_WITHDRAW = 2;
  KIND_TRANSFER = 3;
}
enum FlowDomain {
  DOMAIN_UNSPECIFIED = 0;
  DOMAIN_EXTERNAL_CHAIN = 1;
  DOMAIN_ZIPPER = 2;
  DOMAIN_FUNDING = 3;
  DOMAIN_TRADING = 4;
  DOMAIN_LENDING = 5;
}
enum LifecycleSource {
  SOURCE_UNSPECIFIED = 0;
  SOURCE_RELAYER = 1;
  SOURCE_POLYESTER_CHAIN = 2;
  SOURCE_EXECUTOR = 3;
  SOURCE_LEDGER = 4;
}
enum FlowState {
  STATE_UNSPECIFIED = 0;
  STATE_PENDING_SOURCE = 1;
  STATE_PENDING_POLYESTER_CHAIN = 2;
  STATE_PENDING_LEDGER = 3;
  STATE_COMPLETED = 4;
  STATE_FAILED = 5;
  STATE_DROPPED = 6;
  STATE_REFUNDED = 7;
}
message AssetIds {
  optional 13 zipped_asset_id = 1;
  optional 13 unified_asset_id = 3;
}
message RequestFee {
  optional .chain.lifecycle.v1.AssetIds asset_ids = 1;
  optional .polyester.type.v1.U128 amount_e18 = 2;
  optional 9 recipient_address = 3;
  optional .chain.lifecycle.v1.RequestFeeStatus status = 4;
}
```


## `chain_withdraw_v1_withdraw`

```
// chain/withdraw/v1/withdraw.proto  package=chain.withdraw.v1
enum ErrorCode {
  ERROR_CODE_UNSPECIFIED = 0;
  ERROR_CODE_INSUFFICIENT_FUNDS = 1;
  ERROR_CODE_INVALID_REQUEST = 2;
  ERROR_CODE_UNAUTHENTICATED = 3;
  ERROR_CODE_PERMISSION_DENIED = 4;
  ERROR_CODE_RATE_LIMIT_EXCEEDED = 5;
  ERROR_CODE_SERVICE_UNAVAILABLE = 6;
  ERROR_CODE_INTERNAL_ERROR = 7;
  ERROR_CODE_INVALID_SUBACCOUNT_ID = 8;
  ERROR_CODE_SUBACCOUNT_NOT_FOUND = 9;
  ERROR_CODE_INVALID_ACTION = 10;
  ERROR_CODE_UNSUPPORTED_LEDGER = 11;
  ERROR_CODE_UNSUPPORTED_ASSET = 12;
  ERROR_CODE_INVALID_AMOUNT = 13;
  ERROR_CODE_INVALID_DESTINATION_CHAIN = 14;
  ERROR_CODE_INVALID_DESTINATION_ADDRESS = 15;
  ERROR_CODE_EXTERNAL_DESTINATION_NOT_WHITELISTED = 16;
  ERROR_CODE_INTERNAL_RECIPIENT_NOT_WHITELISTED = 17;
  ERROR_CODE_AMOUNT_BELOW_MINIMUM = 18;
  ERROR_CODE_AMOUNT_EXCEEDS_SUPPLY = 19;
  ERROR_CODE_SOURCE_SMART_ACCOUNT_UNAVAILABLE = 20;
  ERROR_CODE_SIGNATURE_REQUIRED = 21;
  ERROR_CODE_SIGNATURE_SCHEME_UNSUPPORTED = 22;
  ERROR_CODE_SIGNER_WALLET_INVALID = 23;
  ERROR_CODE_WALLET_BINDING_INVALID = 24;
  ERROR_CODE_WALLET_BINDING_SCOPE_MISMATCH = 25;
  ERROR_CODE_WALLET_BINDING_SIGNER_MISMATCH = 26;
  ERROR_CODE_API_KEY_NOT_FOUND = 27;
  ERROR_CODE_API_KEY_BINDING_INVALID = 28;
  ERROR_CODE_API_KEY_BINDING_SCOPE_MISMATCH = 29;
  ERROR_CODE_API_KEY_BINDING_PUBLIC_KEY_MISMATCH = 30;
  ERROR_CODE_IDEMPOTENCY_CONFLICT = 31;
  ERROR_CODE_FUNDS_LOCK_CONFLICT = 32;
  ERROR_CODE_CAPITAL_VIEW_UNAVAILABLE = 33;
  ERROR_CODE_CHAIN_METADATA_UNAVAILABLE = 34;
  ERROR_CODE_FEE_UNAVAILABLE = 35;
  ERROR_CODE_SUPPLY_UNAVAILABLE = 36;
  ERROR_CODE_STEP_UP_UNAVAILABLE = 37;
  ERROR_CODE_DESTINATION_VALIDATION_UNAVAILABLE = 38;
  ERROR_CODE_ACCOUNT_SHARD_UNAVAILABLE = 39;
  ERROR_CODE_FAILED_PRECONDITION = 40;
  ERROR_CODE_NOT_FOUND = 41;
  ERROR_CODE_CONFLICT = 42;
}
enum TradingWithdrawAction {
  ACTION_UNSPECIFIED = 0;
  TO_FUNDING = 1;
  TO_EXTERNAL_CHAIN = 2;
}
enum WithdrawDestinationValidationCode {
  RESULT_UNSPECIFIED = 0;
  VALID = 1;
  INVALID_ADDRESS = 2;
  UNSUPPORTED_CHAIN = 3;
  POLYESTER_SMART_ACCOUNT = 4;
  TOKEN_CONTRACT = 5;
  DENYLISTED_ADDRESS = 6;
}
message CreateTradingWithdrawResponse {
  optional 9 intent_id = 1;
}
message CreateWalletTradingWithdrawResponse {
  optional 9 intent_id = 1;
}
message ErrorDetail {
  optional .chain.withdraw.v1.ErrorCode code = 1;
}
message TradingWithdrawIntentPayload {
  optional .chain.withdraw.v1.TradingWithdrawAction action = 1;
  optional 13 asset_id = 2;
  optional 4 destination_chain_id = 3;
  optional .polyester.type.v1.U128 amount_e18 = 4;
  optional 4 deadline_ts_sec = 5;
  optional .polyester.type.v1.U128 nonce = 6;
  optional 9 destination_address = 7;
  optional 9 idempotency_key = 8;
}
message CreateTradingWithdrawRequest {
  optional .chain.withdraw.v1.TradingWithdrawIntentPayload payload = 1;
  optional 12 payload_signature = 2;
}
message CreateWalletTradingWithdrawRequest {
  optional .chain.withdraw.v1.TradingWithdrawIntentPayload payload = 1;
  optional 4 subaccount_id = 2;
  optional 9 signer_wallet = 3;
  optional 12 payload_signature = 4;
}
message ValidateWithdrawDestinationRequest {
  optional 4 destination_chain_id = 1;
  optional 9 destination_address = 2;
}
message ValidateWithdrawDestinationResponse {
  optional 8 valid = 1;
  optional .chain.withdraw.v1.WithdrawDestinationValidationCode code = 2;
  optional 9 message = 3;
  optional 9 canonical_destination_address = 4;
}
service WithdrawService {
  rpc ValidateWithdrawDestination(.chain.withdraw.v1.ValidateWithdrawDestinationRequest) returns (.chain.withdraw.v1.ValidateWithdrawDestinationResponse);
  rpc CreateTradingWithdraw(.chain.withdraw.v1.CreateTradingWithdrawRequest) returns (.chain.withdraw.v1.CreateTradingWithdrawResponse);
  rpc CreateWalletTradingWithdraw(.chain.withdraw.v1.CreateWalletTradingWithdrawRequest) returns (.chain.withdraw.v1.CreateWalletTradingWithdrawResponse);
}
```


## `chain_zipper_v1_reason`

```
// chain/zipper/v1/reason.proto  package=chain.zipper.v1
enum ZipperReasonCode {
  REASON_UNSPECIFIED = 0;
  DEPOSIT_WAIT_EXPIRED = 1001;
  DEPOSIT_AMOUNT_INVALID = 1002;
  DEPOSIT_AMOUNT_BELOW_MINIMUM = 1003;
  DEPOSIT_AMOUNT_NOT_ABOVE_FEE = 1004;
  DEPOSIT_NET_AMOUNT_BELOW_MINIMUM = 1005;
  EVM_DEPOSIT_SOURCE_TX_INVALID = 1101;
  EVM_DEPOSIT_SOURCE_TX_ZERO = 1102;
  EVM_DEPOSIT_SOURCE_TX_NOT_FOUND = 1103;
  EVM_DEPOSIT_SOURCE_TX_REVERTED = 1104;
  EVM_DEPOSIT_TRANSFER_MISMATCH = 1105;
  UTXO_DEPOSIT_TRANSACTION_MISMATCH = 1201;
  BTC_DEPOSIT_TRANSACTION_MISMATCH = 1202;
  BCH_DEPOSIT_TRANSACTION_MISMATCH = 1203;
  DOGE_DEPOSIT_TRANSACTION_MISMATCH = 1204;
  LTC_DEPOSIT_TRANSACTION_MISMATCH = 1205;
  UTXO_DEPOSIT_SOURCE_IS_DEPOSIT_ADDRESS = 1206;
  SOLANA_DEPOSIT_SIGNATURE_INVALID = 1301;
  SOLANA_DEPOSIT_TRANSACTION_FAILED = 1302;
  SOLANA_DEPOSIT_TRANSFER_MISMATCH = 1303;
  XRP_DEPOSIT_SOURCE_HASH_INDEX_INVALID = 1401;
  XRP_DEPOSIT_SOURCE_ADDRESS_INVALID = 1402;
  XRP_DEPOSIT_ADDRESS_INVALID = 1403;
  XRP_DEPOSIT_PAYMENT_MISMATCH = 1404;
  REJECTION_UNMAPPED = 1999;
  WITHDRAWAL_AMOUNT_INVALID = 2001;
  WITHDRAWAL_AMOUNT_BELOW_MINIMUM = 2002;
  WITHDRAWAL_ASSET_INVALID = 2003;
  WITHDRAWAL_SENDER_INVALID = 2004;
  WITHDRAWAL_DESTINATION_INVALID = 2005;
  WITHDRAWAL_ASSET_UNAVAILABLE = 2006;
  EVM_WITHDRAWAL_DESTINATION_INVALID = 2101;
  BTC_WITHDRAWAL_DESTINATION_INVALID = 2201;
  BCH_WITHDRAWAL_DESTINATION_INVALID = 2202;
  DOGE_WITHDRAWAL_DESTINATION_INVALID = 2203;
  LTC_WITHDRAWAL_DESTINATION_INVALID = 2204;
  SOLANA_WITHDRAWAL_DESTINATION_INVALID = 2301;
  XRP_WITHDRAWAL_CLASSIC_ADDRESS_INVALID = 2401;
  XRP_WITHDRAWAL_DESTINATION_TAG_INVALID = 2402;
  WITHDRAWAL_LIQUIDITY_INSUFFICIENT = 3001;
  COMPLIANCE_HIGH_RISK_ADDRESS = 3002;
  REQUEST_VERIFICATION_REJECTED = 3901;
  REJECTED = 3902;
  ERROR_UNMAPPED = 9000;
  ERROR_NETWORK_UNSUPPORTED = 9001;
  ERROR_REQUEST_PROCESSING_FAILED = 9002;
  ERROR_REQUEST_VERIFICATION_FAILED = 9003;
  ERROR_RESULT_SUBMISSION_FAILED = 9004;
  ERROR_STATUS_UNKNOWN = 9005;
}
message ZipperReasonDetails {
  optional .chain.zipper.v1.ZipperReasonCode code = 1;
  optional 9 reason_id = 2;
  optional 9 message = 3;
}
```


## `chain_zipper_v1_zipper`

```
// chain/zipper/v1/zipper.proto  package=chain.zipper.v1
message ChainConfig {
  optional 13 chain_id = 1;
  optional 9 code = 2;
  optional 9 name = 3;
  optional 9 native_chain_id = 4;
  optional 9 native_currency_symbol = 5;
  optional 9 explorer_url = 6;
  optional 9 icon = 7;
  optional 13 required_confirmations = 8;
  optional 13 confirmation_time_seconds = 9;
  optional 8 is_case_sensitive = 10;
  optional 13 min_address_length = 11;
  optional 13 max_address_length = 12;
}
message AssetChainVariant {
  optional 13 zipped_asset_id = 1;
  optional 13 chain_id = 2;
  optional 8 is_native_asset = 3;
  optional 9 network_fee = 4;
  optional 9 ztoken_address = 6;
  optional 9 source_address = 7;
  optional 13 source_decimals = 8;
  optional 13 ztoken_decimals = 9;
  optional 9 deposit_min_amount = 10;
  optional 9 withdraw_min_amount = 11;
  optional 4 supply_q = 12;
}
message ZippedAssetSupplyUpdate {
  optional 13 zipped_asset_id = 1;
  optional 4 supply_q = 2;
}
message ZippedAssetSupplyBatch {
  repeated .chain.zipper.v1.ZippedAssetSupplyUpdate updates = 1;
}
message AssetConfig {
  optional 9 asset = 1;
  optional 13 ledger_id = 2;
  optional 9 name = 3;
  optional 9 icon = 4;
  optional 13 quantity_scale = 5;
  optional 13 quantity_display_decimals = 6;
  repeated .chain.zipper.v1.AssetChainVariant variants = 7;
  optional 9 u_asset_id = 8;
}
message ChainContractConfig {
  optional 9 name = 1;
  optional 9 address = 2;
  optional 9 type = 3;
  optional 9 description = 4;
  optional 13 version = 5;
}
message GetDepositWithdrawConfigRequest {
}
message GetDepositWithdrawConfigResponse {
  repeated .chain.zipper.v1.ChainConfig chains = 1;
  repeated .chain.zipper.v1.AssetConfig assets = 2;
  optional 4 ts_sec = 3;
  repeated .chain.zipper.v1.ChainContractConfig contracts = 5;
}
service ZipperService {
  rpc GetDepositWithdrawConfig(.chain.zipper.v1.GetDepositWithdrawConfigRequest) returns (.chain.zipper.v1.GetDepositWithdrawConfigResponse);
}
```


## `claims_v1_claims`

```
// claims/v1/claims.proto  package=claims.v1
enum ErrorCode {
  ERROR_CODE_UNSPECIFIED = 0;
  ERROR_CODE_CLAIM_TEMPORARILY_UNAVAILABLE = 1;
  ERROR_CODE_UNAUTHENTICATED = 2;
  ERROR_CODE_RATE_LIMIT_EXCEEDED = 3;
  ERROR_CODE_CLAIM_UNAVAILABLE = 4;
  ERROR_CODE_CONFLICT = 5;
  ERROR_CODE_INVALID_REQUEST = 6;
  ERROR_CODE_REQUEST_TOO_LARGE = 7;
  ERROR_CODE_SERVICE_UNAVAILABLE = 8;
  ERROR_CODE_INTERNAL_ERROR = 9;
  ERROR_CODE_PERMISSION_DENIED = 10;
  ERROR_CODE_FAILED_PRECONDITION = 11;
  ERROR_CODE_SOCIAL_VERIFICATION_REQUIRED = 12;
}
enum ClaimPolicy {
  POLICY_UNSPECIFIED = 0;
  UTC_DAILY = 1;
}
enum DailyClaimState {
  CLAIM_UNSPECIFIED = 0;
  CLAIM_AVAILABLE = 1;
  CLAIM_PROCESSING = 2;
  CLAIM_CLAIMED = 3;
  CLAIM_UNAVAILABLE = 4;
}
message ErrorDetail {
  optional .claims.v1.ErrorCode code = 1;
}
message ClaimCampaign {
  optional 9 campaign_id = 1;
  optional 9 name = 2;
  optional 9 description = 3;
  optional .claims.v1.ClaimPolicy claim_policy = 4;
}
message DailyClaimReward {
  optional 13 asset_id = 1;
  optional 9 asset_code = 2;
  optional .polyester.type.v1.U128 amount_e18 = 3;
}
message GetDailyClaimStatusRequest {
}
message GetDailyClaimStatusResponse {
  optional .claims.v1.DailyClaimState state = 1;
  optional .google.protobuf.Timestamp reset_at = 2;
  repeated .claims.v1.DailyClaimReward rewards = 3;
  optional 9 claim_id = 4;
  optional .claims.v1.ClaimCampaign campaign = 5;
}
message ClaimDailyRewardRequest {
}
message DailyClaimTransfer {
  optional 13 asset_id = 1;
  optional 9 transfer_id = 2;
}
message ClaimDailyRewardResponse {
  optional 9 claim_id = 1;
  optional .claims.v1.DailyClaimState state = 2;
  optional .google.protobuf.Timestamp claimed_at = 3;
  repeated .claims.v1.DailyClaimReward rewards = 4;
  repeated .claims.v1.DailyClaimTransfer transfers = 5;
  optional .google.protobuf.Timestamp reset_at = 6;
  optional .claims.v1.ClaimCampaign campaign = 7;
}
service ClaimsService {
  rpc GetDailyClaimStatus(.claims.v1.GetDailyClaimStatusRequest) returns (.claims.v1.GetDailyClaimStatusResponse);
  rpc ClaimDailyReward(.claims.v1.ClaimDailyRewardRequest) returns (.claims.v1.ClaimDailyRewardResponse);
}
```


## `collab_v1_whiteboard`

```
// collab/v1/whiteboard.proto  package=collab.v1
enum BoardAudience {
  AUDIENCE_UNSPECIFIED = 0;
  PRIVATE = 1;
  PUBLIC = 2;
  FOLLOWERS = 3;
}
enum BoardRole {
  ROLE_UNSPECIFIED = 0;
  VIEWER = 1;
  EDITOR = 2;
  OWNER = 3;
}
enum BoardAclSubjectType {
  SUBJECT_TYPE_UNSPECIFIED = 0;
  USER_SUBJECT = 1;
  GROUP_SUBJECT = 2;
}
message BoardAclEntry {
  optional .collab.v1.BoardAclSubjectType subject_type = 1;
  optional 6 subject_id = 2;
  optional .collab.v1.BoardRole role = 3;
}
message BoardPermissions {
  optional 8 can_view = 1;
  optional 8 can_edit = 2;
  optional 8 can_manage = 3;
}
message BoardAccess {
  optional .collab.v1.BoardRole role = 1;
  optional .collab.v1.BoardPermissions permissions = 2;
}
message Board {
  optional 9 board_id = 1;
  optional 6 owner_account_id = 2;
  optional 9 title = 3;
  optional .collab.v1.BoardAudience audience = 4;
  optional .collab.v1.BoardRole default_role = 5;
  optional 4 access_version = 6;
  optional .google.protobuf.Struct initial_snapshot = 7;
  optional .google.protobuf.Timestamp created_at = 8;
  optional .google.protobuf.Timestamp updated_at = 9;
  optional .google.protobuf.Timestamp archived_at = 10;
}
message BoardListItem {
  optional .collab.v1.Board board = 1;
  optional .collab.v1.BoardAccess access = 2;
}
message PresencePayload {
  optional 6 account_id = 1;
  optional .collab.v1.BoardRole role = 2;
}
message CreateBoardRequest {
  optional 9 title = 1;
  optional .collab.v1.BoardAudience audience = 2;
  optional .collab.v1.BoardRole default_role = 3;
  repeated .collab.v1.BoardAclEntry acl_entries = 4;
  optional .google.protobuf.Struct initial_snapshot = 5;
}
message CreateBoardResponse {
  optional .collab.v1.Board board = 1;
  repeated .collab.v1.BoardAclEntry acl_entries = 2;
  optional .collab.v1.BoardAccess access = 3;
}
message GetBoardRequest {
  optional 9 board_id = 1;
}
message GetBoardResponse {
  optional .collab.v1.Board board = 1;
  repeated .collab.v1.BoardAclEntry acl_entries = 2;
  optional .collab.v1.BoardAccess access = 3;
}
message ListBoardsRequest {
  optional 8 include_archived = 1;
  optional 13 limit = 2;
  optional 9 page_token = 3;
}
message ListBoardsResponse {
  repeated .collab.v1.BoardListItem boards = 1;
  optional 9 next_page_token = 2;
}
message UpdateBoardRequest {
  optional 9 board_id = 1;
  optional 9 title = 2;
  optional .collab.v1.BoardAudience audience = 3;
  optional .collab.v1.BoardRole default_role = 4;
  optional .google.protobuf.Struct initial_snapshot = 5;
}
message UpdateBoardResponse {
  optional .collab.v1.Board board = 1;
  repeated .collab.v1.BoardAclEntry acl_entries = 2;
  optional .collab.v1.BoardAccess access = 3;
}
message UpdateBoardAclRequest {
  optional 9 board_id = 1;
  repeated .collab.v1.BoardAclEntry acl_entries = 2;
}
message UpdateBoardAclResponse {
  optional .collab.v1.Board board = 1;
  repeated .collab.v1.BoardAclEntry acl_entries = 2;
  optional .collab.v1.BoardAccess access = 3;
}
message ArchiveBoardRequest {
  optional 9 board_id = 1;
  optional 8 archived = 2;
}
message ArchiveBoardResponse {
  optional .collab.v1.Board board = 1;
  optional .collab.v1.BoardAccess access = 2;
}
message MintJoinTokenRequest {
  optional 9 board_id = 1;
}
message MintJoinTokenResponse {
  optional 9 board_id = 1;
  optional .collab.v1.BoardAccess access = 2;
  optional .google.protobuf.Timestamp expires_at = 3;
  optional 9 token = 4;
  optional 9 room_id = 5;
  optional 9 connection_id = 6;
  optional 9 socket_path = 7;
  optional .collab.v1.PresencePayload presence = 8;
  optional 4 access_version = 9;
}
service WhiteboardService {
  rpc CreateBoard(.collab.v1.CreateBoardRequest) returns (.collab.v1.CreateBoardResponse);
  rpc GetBoard(.collab.v1.GetBoardRequest) returns (.collab.v1.GetBoardResponse);
  rpc ListBoards(.collab.v1.ListBoardsRequest) returns (.collab.v1.ListBoardsResponse);
  rpc UpdateBoard(.collab.v1.UpdateBoardRequest) returns (.collab.v1.UpdateBoardResponse);
  rpc UpdateBoardAcl(.collab.v1.UpdateBoardAclRequest) returns (.collab.v1.UpdateBoardAclResponse);
  rpc ArchiveBoard(.collab.v1.ArchiveBoardRequest) returns (.collab.v1.ArchiveBoardResponse);
  rpc MintJoinToken(.collab.v1.MintJoinTokenRequest) returns (.collab.v1.MintJoinTokenResponse);
}
```


## `fees_v1_fees`

```
// fees/v1/fees.proto  package=fees.v1
message SpotFeeRate {
  optional 13 symbol_id = 1;
  optional 9 maker_fee_rate_percent = 3;
  optional 9 taker_fee_rate_percent = 4;
  optional 13 vip_tier = 5;
}
message GetSpotFeeRatesRequest {
  optional 6 subaccount_id = 1;
  repeated 13 symbol_id = 2;
}
message GetSpotFeeRatesResponse {
  repeated .fees.v1.SpotFeeRate fee_rates = 1;
}
service FeeService {
  rpc GetSpotFeeRates(.fees.v1.GetSpotFeeRatesRequest) returns (.fees.v1.GetSpotFeeRatesResponse);
}
```


## `ledger_read_v1_ledger_read`

```
// ledger/read/v1/ledger_read.proto  package=ledger.read.v1
enum BalanceRange {
  RANGE_UNSPECIFIED = 0;
  DAY_1 = 1;
  DAY_7 = 2;
  DAY_30 = 3;
  DAY_90 = 4;
  DAY_180 = 5;
  DAY_365 = 6;
}
enum EquityGroupBy {
  GROUP_BY_UNSPECIFIED = 0;
  GROUP_BY_ACCOUNT = 1;
  GROUP_BY_ASSET = 2;
}
enum TransferSideKind {
  TRANSFER_SIDE_KIND_UNSPECIFIED = 0;
  FUNDING_ACCOUNT = 1;
  TRADING_ACCOUNT = 2;
  EXTERNAL_ADDRESS = 3;
  PRIVATE_COUNTERPARTY = 4;
  FEE_ACCOUNT = 5;
  SYSTEM_ACCOUNT = 6;
}
enum ErrorCode {
  ERROR_CODE_UNSPECIFIED = 0;
  ERROR_CODE_BAD_REQUEST = 1;
  ERROR_CODE_UNAUTHENTICATED = 2;
  ERROR_CODE_PERMISSION_DENIED = 3;
  ERROR_CODE_NOT_FOUND = 4;
  ERROR_CODE_MISSING_ACCOUNT_ID = 5;
  ERROR_CODE_INVALID_ACCOUNT_ID = 6;
  ERROR_CODE_MISSING_WALLET = 7;
  ERROR_CODE_WALLET_RESOLUTION_UNAVAILABLE = 8;
  ERROR_CODE_WALLET_NOT_FOUND = 9;
  ERROR_CODE_UPSTREAM_ERROR = 10;
}
message GetBalancesRequest {
  optional 6 subaccount_id = 1;
}
message AssetBalance {
  optional 13 asset_id = 1;
  optional .polyester.type.v1.U128 trading = 2;
  optional .polyester.type.v1.U128 funding = 3;
  optional .polyester.type.v1.U128 reserved = 4;
  optional .polyester.type.v1.U128 available = 5;
  optional 4 trading_revision = 6;
  optional 4 funding_revision = 7;
}
message GetBalancesResponse {
  repeated .ledger.read.v1.AssetBalance balances = 1;
}
message GetBalanceHistoryRequest {
  optional 6 subaccount_id = 1;
  optional .ledger.read.v1.BalanceRange range = 2;
  optional 13 ledger = 3;
  repeated .ledger.v1.AccountCode account_codes = 4;
}
message BalanceSeries {
  optional 13 asset_id = 1;
  optional .ledger.v1.AccountCode account_code = 2;
  repeated 4 balance_q = 3;
}
message GetBalanceHistoryResponse {
  optional .ledger.read.v1.BalanceRange range = 1;
  optional 9 bucket = 2;
  optional 7 start_ts_sec = 3;
  optional 7 end_ts_sec = 4;
  optional 13 points = 5;
  repeated .ledger.read.v1.BalanceSeries series = 6;
}
message AccountGrouping {
  optional 13 account_code = 1;
  optional 9 name = 2;
}
message AssetGrouping {
  optional 13 id = 1;
  optional 9 symbol = 2;
}
message PortfolioAccountGrouping {
  optional 6 account_id = 1;
  optional 8 remaining = 2;
}
message GetEquityHistorySeriesRequest {
  optional 6 subaccount_id = 1;
  optional .ledger.read.v1.BalanceRange range = 2;
  repeated .ledger.v1.AccountCode account_codes = 4;
  optional .ledger.read.v1.EquityGroupBy group_by = 5;
}
message EquitySeries {
  optional .ledger.read.v1.AccountGrouping account = 1;
  optional .ledger.read.v1.AssetGrouping asset = 3;
  optional .ledger.read.v1.PortfolioAccountGrouping portfolio_account = 4;
  repeated 18 equity_q = 2;
}
message GetEquityHistorySeriesResponse {
  optional .ledger.read.v1.BalanceRange range = 1;
  optional 9 bucket = 2;
  optional 7 start_ts_sec = 3;
  optional 7 end_ts_sec = 4;
  optional 9 quote_asset = 6;
  optional 13 points = 7;
  repeated .ledger.read.v1.EquitySeries series = 8;
  repeated 3 btc_prices_q = 10;
}
message GetPortfolioEquityHistorySeriesRequest {
  optional .ledger.read.v1.BalanceRange range = 1;
}
message GetPortfolioEquityHistorySeriesResponse {
  optional .ledger.read.v1.BalanceRange range = 1;
  optional 9 bucket = 2;
  optional 7 start_ts_sec = 3;
  optional 7 end_ts_sec = 4;
  optional 9 quote_asset = 5;
  optional 13 points = 6;
  repeated .ledger.read.v1.EquitySeries series = 7;
  repeated 3 btc_prices_q = 8;
}
message PortfolioAccountEquity {
  optional 6 account_id = 1;
  optional 18 equity_q = 2;
  repeated 13 top_asset_ids = 3;
}
message PortfolioAssetEquity {
  optional 13 asset_id = 1;
  optional 4 balance_q = 2;
  optional 18 equity_q = 3;
}
message GetPortfolioEquitySnapshotRequest {
}
message GetPortfolioEquitySnapshotResponse {
  optional 9 quote_asset = 1;
  optional 18 total_equity_q = 2;
  repeated .ledger.read.v1.PortfolioAccountEquity accounts = 3;
  repeated .ledger.read.v1.PortfolioAssetEquity assets = 4;
  optional 3 btc_price_q = 5;
}
message ListTransfersRequest {
  optional 6 subaccount_id = 1;
  optional 13 limit = 2;
  optional 8 reversed = 3;
  optional 4 ts_min_us = 4;
  optional 4 ts_max_us = 5;
  optional .ledger.v1.TransferCode transfer_code = 6;
  optional 13 ledger = 7;
  optional 9 page_token = 9;
}
message TransferSide {
  optional .ledger.read.v1.TransferSideKind kind = 1;
  optional 6 account_id = 2;
  optional 9 address = 3;
  optional 13 chain_id = 4;
}
message TransferRow {
  optional 13 asset_id = 1;
  optional .polyester.type.v1.U128 amount_e18 = 2;
  optional .ledger.v1.TransferCode transfer_code = 3;
  optional .ledger.v1.AccountCode account_code = 4;
  optional 4 ts_us = 5;
  optional .polyester.type.v1.U128 balance_after_e18 = 9;
  optional 8 is_debit = 10;
  optional 4 link_id = 11;
  optional 9 flow_id = 12;
  optional .ledger.read.v1.TransferSide source = 13;
  optional .ledger.read.v1.TransferSide destination = 14;
}
message ListTransfersResponse {
  repeated .ledger.read.v1.TransferRow transfers = 1;
  optional 9 next_page_token = 3;
}
message ListHoldsRequest {
  optional 6 subaccount_id = 1;
  optional 13 limit = 2;
  optional 8 reversed = 3;
  optional 9 page_token = 4;
}
message HoldRow {
  optional 6 hold_id = 1;
  optional .polyester.type.v1.U128 amount_reserved_e18 = 2;
  optional 13 asset_id = 3;
  optional 4 expires_at_ns = 4;
}
message ListHoldsResponse {
  repeated .ledger.read.v1.HoldRow holds = 1;
  optional 9 next_page_token = 2;
}
message ErrorDetail {
  optional .ledger.read.v1.ErrorCode code = 1;
}
service LedgerReadService {
  rpc GetBalanceHistory(.ledger.read.v1.GetBalanceHistoryRequest) returns (.ledger.read.v1.GetBalanceHistoryResponse);
  rpc GetEquityHistorySeries(.ledger.read.v1.GetEquityHistorySeriesRequest) returns (.ledger.read.v1.GetEquityHistorySeriesResponse);
  rpc GetPortfolioEquityHistorySeries(.ledger.read.v1.GetPortfolioEquityHistorySeriesRequest) returns (.ledger.read.v1.GetPortfolioEquityHistorySeriesResponse);
  rpc GetPortfolioEquitySnapshot(.ledger.read.v1.GetPortfolioEquitySnapshotRequest) returns (.ledger.read.v1.GetPortfolioEquitySnapshotResponse);
  rpc ListTransfers(.ledger.read.v1.ListTransfersRequest) returns (.ledger.read.v1.ListTransfersResponse);
  rpc ListHolds(.ledger.read.v1.ListHoldsRequest) returns (.ledger.read.v1.ListHoldsResponse);
  rpc GetBalances(.ledger.read.v1.GetBalancesRequest) returns (.ledger.read.v1.GetBalancesResponse);
}
```


## `ledger_v1_catalog`

```
// ledger/v1/catalog.proto  package=ledger.v1
enum AccountCode {
  ACCOUNT_CODE_UNSPECIFIED = 0;
  FUNDING = 300;
  TRADING = 301;
}
enum TransferCode {
  TRANSFER_CODE_UNSPECIFIED = 0;
  DEPOSIT = 1000;
  WITHDRAW = 1001;
  MAKER_FEE = 1010;
  TAKER_FEE = 1011;
  INTERNAL_TRANSFER = 1030;
  TRADE_BASE = 1031;
  TRADE_QUOTE = 1032;
  REBATE = 1041;
  FUNDING_TO_TRADING = 1060;
  TRADING_TO_FUNDING = 1061;
  TRADING_WITHDRAW_RESERVE = 1062;
  FUNDING_USER_TRANSFER = 1063;
  TRADING_WITHDRAW_REQUEST_FEE = 1065;
}
```


## `marketdata_v1_heatmap`

```
// marketdata/v1/heatmap.proto  package=marketdata.v1
enum HeatmapInterval {
  INTERVAL_UNSPECIFIED = 0;
  INTERVAL_1S = 1;
  INTERVAL_1M = 2;
  INTERVAL_5M = 3;
  INTERVAL_1H = 4;
}
enum HeatmapDepth {
  DEPTH_UNSPECIFIED = 0;
  DEPTH_1 = 1;
  DEPTH_5 = 2;
  DEPTH_10 = 3;
  DEPTH_20 = 4;
  DEPTH_50 = 5;
  DEPTH_100 = 6;
  DEPTH_200 = 7;
  DEPTH_500 = 8;
  DEPTH_1000 = 9;
}
enum HeatmapQuantityMode {
  QTY_MODE_UNSPECIFIED = 0;
  CLOSE = 1;
  PEAK = 2;
}
message HeatmapTimeRange {
  optional .google.protobuf.Timestamp start_time = 1;
  optional .google.protobuf.Timestamp end_time = 2;
}
message GetOrderbookHeatmapRequest {
  optional 13 symbol_id = 1;
  optional .marketdata.v1.HeatmapInterval interval = 2;
  optional .marketdata.v1.HeatmapDepth depth = 3;
  optional .marketdata.v1.HeatmapTimeRange time_range = 4;
  optional 9 page_token = 5;
  optional 13 limit = 6;
  optional .marketdata.v1.HeatmapQuantityMode quantity_mode = 7;
}
message HeatmapLevels {
  repeated 3 price_ticks = 1;
  repeated 3 qty_scaled = 2;
}
message HeatmapDeltaLevels {
  repeated 3 price_ticks = 1;
  repeated 3 qty_scaled = 2;
}
message HeatmapKeyframe {
  optional 4 ts_sec = 1;
  optional 3 best_bid_ticks = 2;
  optional 3 best_ask_ticks = 3;
  optional 3 mid_ticks = 4;
  optional .marketdata.v1.HeatmapLevels bids = 5;
  optional .marketdata.v1.HeatmapLevels asks = 6;
  optional 4 book_seq = 7;
}
message HeatmapDeltaBucket {
  optional 4 ts_sec = 1;
  optional .marketdata.v1.HeatmapDeltaLevels bids = 2;
  optional .marketdata.v1.HeatmapDeltaLevels asks = 3;
  optional 13 updates_in_bucket = 4;
  optional 4 book_seq_start = 5;
  optional 4 book_seq_end = 6;
}
message HeatmapLiveBucket {
  optional 13 symbol_id = 1;
  optional .marketdata.v1.HeatmapInterval interval = 2;
  optional 4 ts_sec = 3;
  optional 8 is_final = 4;
  optional .marketdata.v1.HeatmapDeltaLevels bids = 5;
  optional .marketdata.v1.HeatmapDeltaLevels asks = 6;
  optional 13 updates_in_bucket = 7;
  optional 4 book_seq_start = 8;
  optional 4 book_seq_end = 9;
  optional .marketdata.v1.HeatmapQuantityMode quantity_mode = 10;
  optional 4 effective_bin_ticks = 11;
}
message HeatmapDeltaChain {
  optional .marketdata.v1.HeatmapKeyframe base_keyframe = 1;
  repeated .marketdata.v1.HeatmapDeltaBucket deltas = 2;
}
message GetOrderbookHeatmapResponse {
  optional 13 symbol_id = 1;
  optional .marketdata.v1.HeatmapInterval interval = 2;
  optional .marketdata.v1.HeatmapDepth depth = 3;
  optional .marketdata.v1.HeatmapDeltaChain chain = 4;
  optional 4 last_persisted_ts_sec = 5;
  optional 4 live_from_book_seq_end = 6;
  optional 8 has_live_anchor = 7;
  optional 9 next_page_token = 8;
  optional 4 server_time_sec = 10;
  optional .marketdata.v1.HeatmapQuantityMode quantity_mode = 11;
  optional .marketdata.v1.HeatmapLiveBucket live_bucket = 12;
}
service HeatmapService {
  rpc GetOrderbookHeatmap(.marketdata.v1.GetOrderbookHeatmapRequest) returns (.marketdata.v1.GetOrderbookHeatmapResponse);
}
```


## `marketdata_v1_marketdata`

```
// marketdata/v1/marketdata.proto  package=marketdata.v1
enum SideFilter {
  SIDE_UNSPECIFIED = 0;
  BUY = 1;
  SELL = 2;
}
enum Timeframe {
  TIMEFRAME_UNSPECIFIED = 0;
  SEC_1 = 1;
  MIN_1 = 2;
  MIN_5 = 3;
  MIN_15 = 4;
  MIN_30 = 5;
  HOUR_1 = 6;
  HOUR_4 = 7;
  DAY_1 = 8;
  HOUR_12 = 9;
  WEEK_1 = 10;
  MONTH_1 = 11;
}
enum PairStatus {
  PAIR_STATUS_UNSPECIFIED = 0;
  PAIR_STATUS_ENABLED = 1;
  PAIR_STATUS_DISABLED = 2;
  PAIR_STATUS_CANCEL_ONLY = 3;
  PAIR_STATUS_POST_ONLY = 4;
  PAIR_STATUS_REDUCE_ONLY = 5;
}
message GetTradesRequest {
  optional 13 symbol_id = 1;
  optional 13 limit = 2;
  optional .google.protobuf.Timestamp start_time = 3;
  optional .google.protobuf.Timestamp end_time = 4;
  optional .marketdata.v1.SideFilter side = 5;
  optional 9 page_token = 6;
}
message MarketTrade {
  optional 13 symbol_id = 1;
  optional 4 match_id = 2;
  optional 8 is_buy = 3;
  optional 3 price_ticks = 4;
  optional 3 qty_scaled = 5;
  optional 4 ts_ns = 6;
}
message GetTradesResponse {
  repeated .marketdata.v1.MarketTrade trades = 1;
  optional 9 next_page_token = 2;
}
message GetCandlesRequest {
  optional 13 symbol_id = 1;
  optional .marketdata.v1.Timeframe timeframe = 2;
  optional 13 limit = 3;
  optional .google.protobuf.Timestamp start_time = 4;
  optional .google.protobuf.Timestamp end_time = 5;
  optional 8 include_incomplete = 6;
  optional 8 include_reference = 7;
  optional 9 page_token = 8;
}
message GetCandlesColumnsRequest {
  optional 13 symbol_id = 1;
  optional .marketdata.v1.Timeframe timeframe = 2;
  optional 13 limit = 3;
  optional .google.protobuf.Timestamp start_time = 4;
  optional .google.protobuf.Timestamp end_time = 5;
  optional 8 include_incomplete = 6;
  optional 8 include_reference = 7;
  optional 9 page_token = 8;
}
message CandlePoint {
  optional 4 ts_sec = 1;
  optional 3 open = 2;
  optional 3 high = 3;
  optional 3 low = 4;
  optional 3 close = 5;
  optional 3 volume = 6;
  optional 8 is_closed = 7;
  optional 9 quote_volume = 8;
}
message GetCandlesResponse {
  optional 13 symbol_id = 1;
  optional .marketdata.v1.Timeframe timeframe = 2;
  repeated .marketdata.v1.CandlePoint candles = 3;
  repeated .marketdata.v1.CandlePoint reference_candles = 4;
  optional 9 next_page_token = 5;
}
message GetCandlesColumnsResponse {
  optional 13 symbol_id = 1;
  optional .marketdata.v1.Timeframe timeframe = 2;
  repeated 4 ts_sec = 3;
  repeated 3 open = 4;
  repeated 3 high = 5;
  repeated 3 low = 6;
  repeated 3 close = 7;
  repeated 3 volume = 8;
  repeated 4 reference_ts_sec = 9;
  repeated 3 reference_open = 10;
  repeated 3 reference_high = 11;
  repeated 3 reference_low = 12;
  repeated 3 reference_close = 13;
  repeated 3 reference_volume = 14;
  optional 9 next_page_token = 15;
  repeated 9 quote_volume = 16;
}
message Candle {
  optional 13 symbol_id = 1;
  optional .marketdata.v1.Timeframe timeframe = 2;
  optional 4 ts_sec = 3;
  optional 3 open = 4;
  optional 3 high = 5;
  optional 3 low = 6;
  optional 3 close = 7;
  optional 3 volume = 8;
  optional 9 quote_volume = 9;
}
message AssetConfig {
  optional 9 asset = 1;
  optional 13 ledger_id = 2;
  optional 9 name = 3;
  optional 13 quantity_display_decimals = 4;
  optional 13 quantity_scale = 5;
  optional 13 market_data_volume_scale = 6;
}
message PairMarketdataConfig {
  repeated 1 orderbook_price_buckets = 1;
}
message PairConfig {
  optional 13 symbol_id = 1;
  optional 9 symbol = 2;
  optional 9 base_asset = 3;
  optional 9 quote_asset = 4;
  optional 9 tick_size = 5;
  optional 9 step_size = 6;
  optional 9 min_notional_quote = 7;
  optional 9 min_qty_base = 8;
  optional 8 allow_buy_fee_from_base = 9;
  optional 13 base_quantity_scale = 10;
  optional 13 quote_quantity_scale = 11;
  optional .marketdata.v1.PairMarketdataConfig marketdata = 12;
  optional .google.protobuf.Timestamp listing_at = 13;
  optional .google.protobuf.Timestamp delisting_at = 14;
  optional .marketdata.v1.PairStatus status = 15;
  optional 5 default_market_slippage_bps_buy = 16;
  optional 5 default_market_slippage_bps_sell = 17;
  optional 5 max_client_ref_drift_bps = 18;
  optional 13 reference_price_scale = 19;
}
message GetSpotConfigRequest {
}
message GetSpotConfigResponse {
  repeated .marketdata.v1.AssetConfig assets = 1;
  repeated .marketdata.v1.PairConfig pairs = 2;
  optional 4 ts_sec = 3;
}
service MarketDataService {
  rpc GetTrades(.marketdata.v1.GetTradesRequest) returns (.marketdata.v1.GetTradesResponse);
  rpc GetCandles(.marketdata.v1.GetCandlesRequest) returns (.marketdata.v1.GetCandlesResponse);
  rpc GetCandlesColumns(.marketdata.v1.GetCandlesColumnsRequest) returns (.marketdata.v1.GetCandlesColumnsResponse);
  rpc GetSpotConfig(.marketdata.v1.GetSpotConfigRequest) returns (.marketdata.v1.GetSpotConfigResponse);
}
```


## `marketoverview_v1_marketoverview`

```
// marketoverview/v1/marketoverview.proto  package=marketoverview.v1
enum SparklineInterval {
  SPARKLINE_INTERVAL_UNSPECIFIED = 0;
  SPARKLINE_1H = 1;
  SPARKLINE_24H = 2;
  SPARKLINE_1W = 3;
  SPARKLINE_1M = 4;
}
enum MarketOrderBy {
  MARKET_ORDER_BY_UNSPECIFIED = 0;
  ORDER_BY_CHANGE_24H_BPS = 1;
  ORDER_BY_VOLUME_24H_USD = 2;
  ORDER_BY_LAST_PRICE = 3;
  ORDER_BY_DATE_ADDED = 4;
}
enum SortDirection {
  SORT_DIRECTION_UNSPECIFIED = 0;
  SORT_ASC = 1;
  SORT_DESC = 2;
}
enum ErrorCode {
  ERROR_CODE_UNSPECIFIED = 0;
  ERROR_CODE_BAD_REQUEST = 1;
  ERROR_CODE_INVALID_ARGUMENT = 2;
  ERROR_CODE_NOT_FOUND = 3;
  ERROR_CODE_UNAVAILABLE = 4;
  ERROR_CODE_UPSTREAM_ERROR = 5;
}
message ErrorDetail {
  optional .marketoverview.v1.ErrorCode code = 1;
}
message Sparkline {
  optional .marketoverview.v1.SparklineInterval interval = 1;
  repeated 3 close_ticks = 2;
}
message MarketOverview {
  optional 13 symbol_id = 1;
  optional 3 last_price_ticks = 3;
  optional 4 last_trade_ts_ns = 4;
  optional 5 change_24h_bps = 5;
  optional 3 high_24h_ticks = 6;
  optional 3 low_24h_ticks = 7;
  optional 3 volume_24h_base_scaled = 8;
  optional 3 volume_24h_quote_scaled = 14;
  optional 3 volume_24h_usd_scaled = 17;
  optional 4 listed_ts_ns = 15;
  optional 3 best_bid_ticks = 9;
  optional 3 best_bid_qty_scaled = 10;
  optional 3 best_ask_ticks = 11;
  optional 3 best_ask_qty_scaled = 12;
  repeated .marketoverview.v1.Sparkline sparklines = 13;
  optional 3 index_price_ticks = 16;
}
message ListMarketOverviewRequest {
  repeated 13 symbol_id = 1;
  optional 13 limit = 2;
  optional 9 page_token = 3;
  optional .marketoverview.v1.MarketOrderBy order_by = 4;
  optional .marketoverview.v1.SortDirection sort = 5;
  optional 8 include_sparklines = 6;
  repeated .marketoverview.v1.SparklineInterval sparkline_intervals = 7;
}
message ListMarketOverviewResponse {
  repeated .marketoverview.v1.MarketOverview markets = 1;
  optional 9 next_page_token = 2;
}
message MarketOverviewBatch {
  repeated .marketoverview.v1.MarketOverview markets = 1;
  optional 4 ts_ns = 2;
}
message GetSpotVolumeHistoryRequest {
  repeated 13 symbol_id = 1;
}
message SpotPairVolumeSeries {
  optional 13 symbol_id = 1;
  repeated 18 volume_usd_scaled = 2;
}
message GetSpotVolumeHistoryResponse {
  optional 9 bucket = 1;
  optional 7 start_ts_sec = 2;
  optional 7 end_ts_sec = 3;
  optional 13 points = 4;
  repeated .marketoverview.v1.SpotPairVolumeSeries pairs = 5;
  repeated 18 total_volume_usd_scaled = 6;
}
message CurrencyMetadata {
  optional 9 code = 1;
  optional 9 default_english_name = 2;
  optional 9 symbol = 3;
  optional 13 fraction_digits = 4;
}
message GetCurrencyConversionConfigRequest {
}
message GetCurrencyConversionConfigResponse {
  repeated .marketoverview.v1.CurrencyMetadata fiat = 1;
  repeated .marketoverview.v1.CurrencyMetadata stablecoins = 2;
}
message FiatConversionRate {
  optional 9 code = 1;
  optional 3 units_per_usd_e8 = 2;
}
message FiatConversionSnapshot {
  repeated .marketoverview.v1.FiatConversionRate rates = 1;
  optional 4 source_ts_sec = 2;
  optional 8 stale = 3;
}
message StablecoinConversionRate {
  optional 9 code = 1;
  optional 3 usd_per_unit_e8 = 2;
  optional 4 source_ts_sec = 3;
  optional 8 stale = 4;
}
message GetCurrencyConversionRatesRequest {
}
message GetCurrencyConversionRatesResponse {
  optional .marketoverview.v1.FiatConversionSnapshot fiat = 1;
  repeated .marketoverview.v1.StablecoinConversionRate stablecoins = 2;
  optional 4 snapshot_ts_sec = 3;
}
service MarketOverviewService {
  rpc GetCurrencyConversionConfig(.marketoverview.v1.GetCurrencyConversionConfigRequest) returns (.marketoverview.v1.GetCurrencyConversionConfigResponse);
  rpc GetCurrencyConversionRates(.marketoverview.v1.GetCurrencyConversionRatesRequest) returns (.marketoverview.v1.GetCurrencyConversionRatesResponse);
  rpc GetSpotVolumeHistory(.marketoverview.v1.GetSpotVolumeHistoryRequest) returns (.marketoverview.v1.GetSpotVolumeHistoryResponse);
  rpc ListMarketOverview(.marketoverview.v1.ListMarketOverviewRequest) returns (.marketoverview.v1.ListMarketOverviewResponse);
}
```


## `orderbook_v1_orderbook`

```
// orderbook/v1/orderbook.proto  package=orderbook.v1
enum Depth {
  DEPTH_UNSPECIFIED = 0;
  DEPTH_1 = 1;
  DEPTH_5 = 2;
  DEPTH_10 = 3;
  DEPTH_20 = 4;
  DEPTH_50 = 5;
  DEPTH_100 = 6;
  DEPTH_200 = 7;
  DEPTH_500 = 8;
  DEPTH_1000 = 9;
}
message GetOrderBookRequest {
  optional 13 symbol_id = 1;
  optional .orderbook.v1.Depth depth = 2;
}
message PriceLevel {
  optional 3 price_ticks = 1;
  optional 3 qty_scaled = 2;
}
message GetOrderBookResponse {
  optional 13 symbol_id = 1;
  optional 4 book_seq = 2;
  repeated .orderbook.v1.PriceLevel bids = 3;
  repeated .orderbook.v1.PriceLevel asks = 4;
  optional .google.protobuf.Timestamp ts = 5;
}
message OrderBookDelta {
  optional 13 symbol_id = 1;
  optional 4 book_seq_start = 2;
  optional 4 book_seq_end = 3;
  repeated .orderbook.v1.PriceLevel bids = 4;
  repeated .orderbook.v1.PriceLevel asks = 5;
  optional 8 reset = 6;
  optional .google.protobuf.Timestamp ts = 7;
}
service OrderbookService {
  rpc GetOrderBook(.orderbook.v1.GetOrderBookRequest) returns (.orderbook.v1.GetOrderBookResponse);
}
```


## `orders_v1_orders`

```
// orders/v1/orders.proto  package=orders.v1
enum Side {
  SIDE_UNSPECIFIED = 0;
  BUY = 1;
  SELL = 2;
}
enum OrderType {
  ORDER_TYPE_UNSPECIFIED = 0;
  LIMIT = 1;
  MARKET = 2;
}
enum TimeInForce {
  TIME_IN_FORCE_UNSPECIFIED = 0;
  GTC = 1;
  IOC = 2;
  FOK = 3;
  GTD = 4;
}
enum FeeAsset {
  FEE_ASSET_UNSPECIFIED = 0;
  QUOTE = 1;
  BASE = 2;
}
enum SelfTradePreventionMode {
  SELF_TRADE_PREVENTION_MODE_UNSPECIFIED = 0;
  EXPIRE_MAKER = 1;
  EXPIRE_TAKER = 2;
  EXPIRE_BOTH = 3;
}
enum ErrorCode {
  ERROR_CODE_UNSPECIFIED = 0;
  ERROR_CODE_BAD_REQUEST = 1;
  ERROR_CODE_INVALID_ARGUMENT = 2;
  ERROR_CODE_INSUFFICIENT_FUNDS = 3;
  ERROR_CODE_UNKNOWN_SYMBOL = 4;
  ERROR_CODE_BAD_PRICE = 5;
  ERROR_CODE_BAD_QTY = 6;
  ERROR_CODE_MIN_NOTIONAL = 7;
  ERROR_CODE_QTY_STEP_SIZE = 8;
  ERROR_CODE_CONFLICT_DUPLICATE_CLIENT_ORDER_ID = 9;
  ERROR_CODE_UNAVAILABLE = 10;
  ERROR_CODE_UNAUTHENTICATED = 11;
  ERROR_CODE_PERMISSION_DENIED = 12;
  ERROR_CODE_NOT_FOUND = 13;
  ERROR_CODE_UPSTREAM_ERROR = 14;
  ERROR_CODE_FEE_ASSET_NOT_ALLOWED = 15;
  ERROR_CODE_PAIR_DISABLED = 16;
  ERROR_CODE_ORDER_UNKNOWN = 17;
  ERROR_CODE_INTERNAL_ERROR = 18;
  ERROR_CODE_SUBACCOUNT_INACTIVE = 19;
  ERROR_CODE_POLICY_MARKET_DENY = 20;
  ERROR_CODE_POLICY_MAX_NOTIONAL = 21;
  ERROR_CODE_POLICY_TRADING_HALTED = 22;
  ERROR_CODE_POLICY_SPOT_TRADE_DENY = 23;
  ERROR_CODE_API_KEY_ROOT_SCOPE_ONLY = 24;
  ERROR_CODE_API_KEY_SUB_SCOPE_ONLY = 25;
  ERROR_CODE_API_KEY_SUBACCOUNT_MISMATCH = 26;
  ERROR_CODE_API_KEY_POLICY_REQUIRED = 27;
  ERROR_CODE_API_KEY_UNKNOWN = 28;
  ERROR_CODE_API_KEY_MARKET_DENY = 29;
  ERROR_CODE_PRICE_TICK_SIZE = 30;
  ERROR_CODE_MIN_QTY = 31;
  ERROR_CODE_POST_ONLY_LIMIT_ONLY = 32;
  ERROR_CODE_BATCH_TOO_LARGE = 33;
  ERROR_CODE_POLICY_MAX_OPEN_ORDERS = 34;
  ERROR_CODE_MODIFICATION_REQUIRES_REPLACE = 35;
  ERROR_CODE_CONFLICT_IDEMPOTENCY_KEY_REUSE = 36;
  ERROR_CODE_MARKET_PRICE_UNAVAILABLE = 37;
  ERROR_CODE_PAIR_NOT_LISTED_YET = 50;
  ERROR_CODE_PAIR_DELISTED = 51;
  ERROR_CODE_PAIR_CANCEL_ONLY = 52;
  ERROR_CODE_PAIR_POST_ONLY = 53;
  ERROR_CODE_PAIR_REDUCE_ONLY = 54;
  ERROR_CODE_RISK_LIMIT = 55;
  ERROR_CODE_MARKET_HALTED = 56;
  ERROR_CODE_ACCOUNT_UNKNOWN = 57;
  ERROR_CODE_POST_ONLY_CROSS = 58;
  ERROR_CODE_REDUCE_ONLY_BLOCKED = 59;
  ERROR_CODE_PRICE_BAND_VIOLATION = 60;
  ERROR_CODE_MARKET_CAP_VIOLATION = 61;
  ERROR_CODE_EMPTY_BOOK = 62;
  ERROR_CODE_FOK_INSUFFICIENT_LIQUIDITY = 63;
  ERROR_CODE_ORDER_ALREADY_TERMINAL = 64;
  ERROR_CODE_TRIGGER_PRICE_INVALID = 40;
  ERROR_CODE_TRIGGER_PRICE_SOURCE_UNSUPPORTED = 41;
  ERROR_CODE_TRAILING_DISTANCE_INVALID = 42;
  ERROR_CODE_TRIGGER_NOT_FOUND = 43;
  ERROR_CODE_TRIGGER_CANCEL_REJECTED = 44;
  ERROR_CODE_TRIGGER_STATUS_INVALID = 45;
  ERROR_CODE_TRIGGER_NOT_MODIFIABLE = 46;
  ERROR_CODE_CONFLICT_DUPLICATE_CLIENT_TRIGGER_ID = 47;
  ERROR_CODE_MAX_SLIPPAGE_INVALID = 48;
  ERROR_CODE_STALE_QUOTE = 65;
  ERROR_CODE_VALIDATION_ERROR = 66;
  ERROR_CODE_OVERLOADED = 67;
  ERROR_CODE_MAX_QUOTE_DEBIT_TOO_SMALL = 68;
  ERROR_CODE_RATE_LIMIT_EXCEEDED = 69;
  ERROR_CODE_SUBACCOUNT_READ_FORBIDDEN = 70;
  ERROR_CODE_POLICY_SPOT_READ_DENY = 71;
  ERROR_CODE_API_KEY_SPOT_READ_DENY = 72;
  ERROR_CODE_CANCEL_REQUEST_EXPIRED = 73;
}
enum TriggerPriceSource {
  TRIGGER_PRICE_SOURCE_UNSPECIFIED = 0;
  LAST_PRICE = 1;
  INDEX_PRICE = 2;
  MARK_PRICE = 3;
}
enum TriggerDirection {
  TRIGGER_DIRECTION_UNSPECIFIED = 0;
  ABOVE = 1;
  BELOW = 2;
}
enum ModifyBehavior {
  MODIFY_BEHAVIOR_UNSPECIFIED = 0;
  AMEND_OR_REPLACE = 1;
  AMEND_ONLY = 2;
  REPLACE_ONLY = 3;
}
enum ModifyActionTaken {
  MODIFY_ACTION_UNSPECIFIED = 0;
  AMENDED = 1;
  REPLACED = 2;
}
enum BatchReplaceAdmissionStatus {
  BATCH_REPLACE_ADMISSION_STATUS_UNSPECIFIED = 0;
  BATCH_REPLACE_ADMISSION_STATUS_ADMITTED = 1;
  BATCH_REPLACE_ADMISSION_STATUS_PARTIALLY_ADMITTED = 2;
  BATCH_REPLACE_ADMISSION_STATUS_REJECTED = 3;
}
enum BatchReplaceItemAdmissionStatus {
  BATCH_REPLACE_ITEM_ADMISSION_STATUS_UNSPECIFIED = 0;
  BATCH_REPLACE_ITEM_ADMISSION_STATUS_ADMITTED = 1;
  BATCH_REPLACE_ITEM_ADMISSION_STATUS_REJECTED = 2;
}
message MarketIoc {
  optional 3 max_slippage_ticks = 1;
  optional 5 max_slippage_bps = 2;
  optional 3 client_ref_price_ticks = 3;
}
message LimitGtc {
  optional 3 price_ticks = 1;
  optional 8 post_only = 2;
}
message LimitGtd {
  optional 3 price_ticks = 1;
  optional 8 post_only = 2;
  optional .google.protobuf.Timestamp expire_at = 3;
}
message LimitIoc {
  optional 3 price_ticks = 1;
}
message LimitFok {
  optional 3 price_ticks = 1;
}
message OrderIntent {
  optional 13 symbol_id = 1;
  optional .orders.v1.Side side = 2;
  optional 3 base_qty_scaled = 3;
  optional 3 max_quote_debit_scaled = 4;
  optional .orders.v1.MarketIoc market_ioc = 10;
  optional .orders.v1.LimitGtc limit_gtc = 11;
  optional .orders.v1.LimitIoc limit_ioc = 12;
  optional .orders.v1.LimitFok limit_fok = 13;
  optional .orders.v1.LimitGtd limit_gtd = 14;
  optional 9 client_order_id = 20;
  optional .orders.v1.FeeAsset fee_asset = 21;
  optional .orders.v1.SelfTradePreventionMode self_trade_prevention_mode = 22;
  optional .orders.v1.RiskPolicy attached_risk = 30;
}
message CreateOrderRequest {
  optional 6 subaccount_id = 1;
  optional .orders.v1.OrderIntent order = 2;
}
message CreateOrderResponse {
  optional 6 order_id = 1;
  optional 9 client_order_id = 2;
  optional .google.protobuf.Timestamp accepted_at = 3;
  optional 4 accepted_at_ts_ns = 4;
  optional 3 resolved_base_qty_scaled = 5;
  optional 3 submitted_max_quote_debit_scaled = 6;
  optional 4 take_profit_trigger_id = 20;
  optional 4 stop_loss_trigger_id = 21;
  optional 4 trailing_stop_trigger_id = 22;
}
message PreviewOrderRequest {
  optional 6 subaccount_id = 1;
  optional .orders.v1.OrderIntent order = 2;
}
message PreviewOrderResponse {
  optional 8 admissible = 1;
  optional .orders.v1.ErrorDetail rejection = 2;
  optional 3 resolved_base_qty_scaled = 3;
  optional 3 protected_price_bound_ticks = 4;
  optional .google.protobuf.Timestamp evaluated_at = 5;
}
message CancelOrderRequest {
  optional 6 order_id = 1;
  optional 9 client_order_id = 2;
  optional 13 symbol_id = 3;
  optional 6 subaccount_id = 4;
}
message CancelOrderResponse {
  optional .orders.v1.CancelOrderResponse.Status status = 1;
  optional 6 order_id = 2;
  optional .google.protobuf.Timestamp ts = 3;
  optional 4 ts_ns = 4;
}
message FieldViolation {
  optional 9 field_path = 1;
  optional 9 rule_id = 2;
  optional 9 message = 3;
}
message ErrorDetail {
  optional .orders.v1.ErrorCode code = 1;
  repeated .orders.v1.FieldViolation violations = 2;
  optional .polyester.ratelimit.v1.RateLimitDetail rate_limit = 3;
}
message RiskMarketIoc {
}
message RiskLimitGtc {
  optional 3 price_ticks = 1;
}
message RiskExecution {
  optional .orders.v1.RiskMarketIoc market_ioc = 1;
  optional .orders.v1.RiskLimitGtc limit_gtc = 2;
}
message TakeProfitPolicy {
  optional 3 trigger_price_ticks = 1;
  optional .orders.v1.RiskExecution child = 2;
}
message StopLossPolicy {
  optional 3 trigger_price_ticks = 1;
  optional .orders.v1.RiskExecution child = 2;
}
message TrailingStopPolicy {
  optional 3 trailing_distance_ticks = 1;
  optional 5 trailing_distance_bps = 2;
  optional 3 max_slippage_ticks = 6;
  optional 5 max_slippage_bps = 7;
  optional 3 activation_price_ticks = 3;
}
message RiskPolicy {
  optional .orders.v1.TakeProfitPolicy take_profit = 1;
  optional .orders.v1.StopLossPolicy stop_loss = 2;
  optional .orders.v1.TrailingStopPolicy trailing_stop = 3;
  optional 8 oco = 4;
}
message CancelAllOrdersRequest {
  optional 6 subaccount_id = 1;
  repeated 13 symbol_ids = 2;
  optional .orders.v1.Side side = 3;
  optional 8 dry_run = 4;
  optional 9 request_id = 6;
}
message CancelAllOrdersResponse {
  optional .orders.v1.CancelAllOrdersResponse.Status status = 1;
  optional 13 matched_orders = 2;
  optional 13 submitted_cancels = 3;
  optional 13 failed_cancels = 4;
  optional .google.protobuf.Timestamp ts = 5;
  optional 4 ts_ns = 6;
}
message CancelAllAfterRequest {
  optional 6 subaccount_id = 1;
  optional 13 timeout_sec = 2;
  optional 13 symbol_id = 3;
  optional .orders.v1.Side side = 4;
  optional 9 request_id = 5;
}
message CancelAllAfterResponse {
  optional .orders.v1.CancelAllAfterResponse.Status status = 1;
  optional 13 effective_timeout_sec = 2;
  optional 4 expires_at_ts_ns = 3;
  optional .google.protobuf.Timestamp ts = 4;
  optional 4 ts_ns = 5;
}
message BatchCreateAccepted {
  optional 6 order_id = 1;
  optional 4 take_profit_trigger_id = 2;
  optional 4 stop_loss_trigger_id = 3;
  optional 4 trailing_stop_trigger_id = 4;
  optional 3 resolved_base_qty_scaled = 5;
  optional 3 submitted_max_quote_debit_scaled = 6;
}
message BatchCreateRejected {
  optional .orders.v1.ErrorDetail error = 1;
}
message BatchCreateResultItem {
  optional 9 client_order_id = 1;
  optional .orders.v1.BatchCreateAccepted accepted = 2;
  optional .orders.v1.BatchCreateRejected rejected = 3;
}
message BatchCreateOrdersRequest {
  optional 6 subaccount_id = 1;
  optional 9 request_id = 2;
  repeated .orders.v1.OrderIntent items = 3;
}
message BatchCreateOrdersResponse {
  repeated .orders.v1.BatchCreateResultItem results = 1;
  optional 13 accepted_count = 2;
  optional 13 rejected_count = 3;
  optional .google.protobuf.Timestamp ts = 4;
  optional 4 ts_ns = 5;
}
message ModifyOrderRequest {
  optional 6 subaccount_id = 1;
  optional 6 order_id = 2;
  optional 9 client_order_id = 3;
  optional 9 request_id = 4;
  optional 3 new_price_ticks = 5;
  optional 3 new_qty_scaled = 6;
  optional .orders.v1.RiskPolicy new_attached_risk = 7;
  optional .orders.v1.ModifyBehavior behavior = 8;
  optional 9 new_client_order_id = 9;
  optional 13 symbol_id = 10;
}
message ModifyOrderResponse {
  optional .orders.v1.ModifyActionTaken action_taken = 1;
  optional 6 old_order_id = 2;
  optional 6 final_order_id = 3;
  optional 9 code = 4;
  optional 4 take_profit_trigger_id = 5;
  optional 4 stop_loss_trigger_id = 6;
  optional 4 trailing_stop_trigger_id = 7;
  optional .google.protobuf.Timestamp ts = 8;
  optional 4 ts_ns = 9;
}
message BatchReplaceOrderItem {
  optional 6 order_id = 1;
  optional 9 client_order_id = 2;
  optional 3 new_price_ticks = 3;
  optional 3 new_qty_scaled = 4;
  optional .orders.v1.RiskPolicy new_attached_risk = 5;
  optional 9 new_client_order_id = 6;
}
message BatchReplaceAdmissionItem {
  optional 13 item_index = 1;
  optional .orders.v1.BatchReplaceItemAdmissionStatus status = 2;
  optional 6 old_order_id = 3;
  optional 6 replacement_order_id = 4;
  optional 9 client_order_id = 5;
  optional 9 code = 6;
  optional .orders.v1.ErrorDetail error = 7;
  optional .orders.v1.ModifyActionTaken action_taken = 8;
}
message BatchReplaceOrdersRequest {
  optional 6 subaccount_id = 1;
  optional 13 symbol_id = 2;
  optional 9 request_id = 3;
  repeated .orders.v1.BatchReplaceOrderItem items = 4;
}
message BatchReplaceOrdersResponse {
  optional 6 batch_request_id = 1;
  optional .orders.v1.BatchReplaceAdmissionStatus status = 2;
  repeated .orders.v1.BatchReplaceAdmissionItem results = 3;
  optional 13 accepted_count = 4;
  optional 13 rejected_count = 5;
  optional .google.protobuf.Timestamp accepted_ts = 6;
  optional 4 accepted_ts_ns = 7;
}
message BatchCancelItem {
  optional 6 order_id = 1;
  optional 9 client_order_id = 2;
  optional 13 symbol_id = 3;
}
message BatchCancelResultItem {
  optional .orders.v1.BatchCancelResultItem.Status status = 1;
  optional 6 order_id = 2;
  optional 9 client_order_id = 3;
  optional 9 code = 4;
  optional .orders.v1.ErrorDetail error = 5;
}
message BatchCancelOrdersRequest {
  optional 6 subaccount_id = 1;
  optional 9 request_id = 2;
  repeated .orders.v1.BatchCancelItem items = 3;
}
message BatchCancelOrdersResponse {
  repeated .orders.v1.BatchCancelResultItem results = 1;
  optional 13 accepted_count = 2;
  optional 13 rejected_count = 3;
  optional .google.protobuf.Timestamp ts = 4;
  optional 4 ts_ns = 5;
}
service OrdersService {
  rpc PreviewOrder(.orders.v1.PreviewOrderRequest) returns (.orders.v1.PreviewOrderResponse);
  rpc CreateOrder(.orders.v1.CreateOrderRequest) returns (.orders.v1.CreateOrderResponse);
  rpc CancelOrder(.orders.v1.CancelOrderRequest) returns (.orders.v1.CancelOrderResponse);
  rpc CancelAllOrders(.orders.v1.CancelAllOrdersRequest) returns (.orders.v1.CancelAllOrdersResponse);
  rpc CancelAllAfter(.orders.v1.CancelAllAfterRequest) returns (.orders.v1.CancelAllAfterResponse);
  rpc BatchCreateOrders(.orders.v1.BatchCreateOrdersRequest) returns (.orders.v1.BatchCreateOrdersResponse);
  rpc ModifyOrder(.orders.v1.ModifyOrderRequest) returns (.orders.v1.ModifyOrderResponse);
  rpc BatchReplaceOrders(.orders.v1.BatchReplaceOrdersRequest) returns (.orders.v1.BatchReplaceOrdersResponse);
  rpc BatchCancelOrders(.orders.v1.BatchCancelOrdersRequest) returns (.orders.v1.BatchCancelOrdersResponse);
}
```


## `orders_v1_orders_read`

```
// orders/v1/orders_read.proto  package=orders.v1
enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  PENDING = 1;
  PENDING_CANCEL = 2;
  WORKING = 3;
  FILLED = 4;
  CANCELED = 5;
  REJECTED = 6;
}
enum BatchReplacePhase {
  BATCH_REPLACE_PHASE_UNSPECIFIED = 0;
  BATCH_REPLACE_PHASE_ADMITTED = 1;
  BATCH_REPLACE_PHASE_WORKING = 2;
  BATCH_REPLACE_PHASE_REJECTED = 3;
  BATCH_REPLACE_PHASE_TERMINAL = 4;
}
enum OrderOriginScope {
  ORDER_ORIGIN_SCOPE_UNSPECIFIED = 0;
  DIRECT = 1;
  ATTACHED_RISK = 2;
  STANDALONE_TRIGGER = 3;
  SYSTEM = 4;
}
enum OrderTriggerType {
  ORDER_TRIGGER_TYPE_UNSPECIFIED = 0;
  STOP_LOSS = 1;
  TAKE_PROFIT = 2;
  TRAILING_STOP = 3;
  TWAP = 4;
  LADDER = 5;
}
message OrderOrigin {
  optional .orders.v1.OrderOriginScope scope = 1;
  optional .orders.v1.OrderTriggerType trigger_type = 2;
  optional 6 trigger_id = 3;
  optional 6 parent_order_id = 4;
  optional 13 child_seq = 5;
}
message AttachedRiskLegState {
  optional .orders.v1.AttachedRiskLegState.Status status = 1;
  optional 4 armed_ts_ns = 2;
  optional 4 terminal_ts_ns = 3;
  optional 6 trigger_id = 4;
  optional 6 child_order_id = 5;
}
message AttachedRiskTakeProfit {
  optional .orders.v1.TakeProfitPolicy policy = 1;
  optional .orders.v1.AttachedRiskLegState state = 2;
}
message AttachedRiskStopLoss {
  optional .orders.v1.StopLossPolicy policy = 1;
  optional .orders.v1.AttachedRiskLegState state = 2;
}
message AttachedRiskTrailingStop {
  optional .orders.v1.TrailingStopPolicy policy = 1;
  optional .orders.v1.AttachedRiskLegState state = 2;
}
message AttachedRisk {
  optional .orders.v1.AttachedRiskTakeProfit take_profit = 1;
  optional .orders.v1.AttachedRiskStopLoss stop_loss = 2;
  optional .orders.v1.AttachedRiskTrailingStop trailing_stop = 3;
  optional 8 oco = 4;
}
message OrderLineage {
  optional 6 id = 1;
  optional 13 generation = 2;
}
message Order {
  optional 6 order_id = 1;
  optional 13 symbol_id = 3;
  optional 9 client_order_id = 4;
  optional .orders.v1.Side side = 5;
  optional .orders.v1.OrderStatus status = 6;
  optional .orders.v1.OrderType order_type = 7;
  optional .orders.v1.TimeInForce time_in_force = 8;
  optional .orders.v1.SelfTradePreventionMode self_trade_prevention_mode = 9;
  optional .orders.v1.FeeAsset fee_asset = 10;
  optional 8 post_only = 11;
  optional 3 orig_qty_scaled = 12;
  optional 3 cum_qty_scaled = 13;
  optional 3 inherited_cum_qty_scaled = 33;
  optional 3 leaves_qty_scaled = 20;
  optional 3 avg_price_ticks = 14;
  optional 3 price_ticks = 15;
  optional 4 created_ts_ns = 16;
  optional 4 terminal_ts_ns = 17;
  optional 13 terminal_reason_code = 18;
  optional 9 terminal_reason = 19;
  optional .orders.v1.AttachedRisk attached_risk = 21;
  optional .orders.v1.OrderOrigin origin = 22;
  optional 3 market_client_ref_price_ticks = 23;
  optional 3 market_max_slippage_ticks = 24;
  optional 5 market_max_slippage_bps = 25;
  optional 13 version = 26;
  optional 6 batch_request_id = 27;
  optional 3 submitted_max_quote_debit_scaled = 28;
  optional .orders.v1.OrderLineage lineage = 31;
  optional .google.protobuf.Timestamp expire_at = 32;
}
message UserTrade {
  optional 13 symbol_id = 2;
  optional 4 match_id = 3;
  optional 6 order_id = 4;
  optional .orders.v1.Side side = 5;
  optional 8 is_maker = 6;
  optional 3 price_ticks = 7;
  optional 3 qty_scaled = 8;
  optional .polyester.type.v1.U128 fee_amount_e18 = 9;
  optional .orders.v1.FeeAsset fee_asset = 10;
  optional .polyester.type.v1.U128 referral_share_amount_e18 = 12;
  optional 4 ts_ns = 13;
  optional 8 fee_is_rebate = 14;
  optional .orders.v1.OrderLineage lineage = 17;
}
message OrderTransfer {
  optional 4 match_id = 1;
  optional 13 symbol_id = 10;
  optional 13 asset_id = 2;
  optional .polyester.type.v1.U128 amount_e18 = 3;
  optional 8 is_debit = 5;
  optional .ledger.v1.TransferCode transfer_code = 6;
  optional .ledger.v1.AccountCode account_code = 7;
  optional 4 ts_ns = 8;
  optional 9 tx_id = 9;
}
message GetOpenOrdersRequest {
  optional 6 subaccount_id = 1;
  repeated 13 symbol_id = 2;
  optional .orders.v1.Side side = 3;
  optional 13 limit = 10;
  optional 9 page_token = 11;
  optional 8 include_attached_risk = 12;
  optional 8 include_attached_risk_state = 13;
  optional 6 trigger_id = 14;
}
message GetOpenOrdersResponse {
  repeated .orders.v1.Order orders = 1;
  optional 9 next_page_token = 2;
}
message GetOrderHistoryRequest {
  optional 6 subaccount_id = 1;
  repeated 13 symbol_id = 2;
  optional .orders.v1.Side side = 3;
  optional .orders.v1.OrderStatus status = 4;
  optional 4 start_ts_ns = 10;
  optional 4 end_ts_ns = 11;
  optional 13 limit = 12;
  optional 9 page_token = 13;
  optional 8 include_attached_risk = 14;
  optional 8 include_attached_risk_state = 15;
  optional 6 trigger_id = 16;
}
message GetOrderHistoryResponse {
  repeated .orders.v1.Order orders = 1;
  optional 9 next_page_token = 2;
}
message GetUserTradesRequest {
  optional 6 subaccount_id = 1;
  optional 13 symbol_id = 2;
  optional .orders.v1.Side side = 3;
  optional 4 start_ts_ns = 10;
  optional 4 end_ts_ns = 11;
  optional 13 limit = 12;
  optional 9 page_token = 13;
  optional 4 after_match_id = 14;
  optional 6 order_id = 15;
  optional 6 lineage_id = 16;
  optional 13 through_generation = 17;
  optional 8 include_transfers = 18;
}
message GetUserTradesResponse {
  repeated .orders.v1.UserTrade trades = 1;
  optional 9 next_page_token = 2;
  repeated .orders.v1.OrderTransfer transfers = 3;
}
message GetOrderRequest {
  optional 6 subaccount_id = 1;
  optional 6 order_id = 2;
  optional 9 client_order_id = 3;
  optional 8 include_attached_risk = 10;
  optional 8 include_attached_risk_state = 11;
  optional 8 include_execution_history = 12;
  optional 13 limit = 13;
  optional 9 page_token = 14;
}
message GetOrderResponse {
  optional .orders.v1.Order order = 1;
  repeated .orders.v1.UserTrade trades = 2;
  repeated .orders.v1.OrderTransfer transfers = 3;
  optional 9 next_page_token = 6;
}
message GetBatchReplaceStatusRequest {
  optional 6 subaccount_id = 1;
  optional 6 batch_request_id = 2;
}
message BatchReplaceStatusItem {
  optional 13 item_index = 1;
  optional .orders.v1.BatchReplacePhase phase = 2;
  optional 6 old_order_id = 3;
  optional 6 replacement_order_id = 4;
  optional .orders.v1.OrderStatus order_status = 5;
  optional 9 code = 6;
  optional 4 updated_ts_ns = 7;
  optional .orders.v1.ModifyActionTaken action_taken = 8;
}
message GetBatchReplaceStatusResponse {
  optional 6 batch_request_id = 1;
  optional .orders.v1.BatchReplaceAdmissionStatus admission_status = 2;
  repeated .orders.v1.BatchReplaceStatusItem items = 3;
  optional 13 accepted_count = 4;
  optional 13 rejected_count = 5;
  optional 4 accepted_ts_ns = 6;
  optional 4 updated_ts_ns = 7;
}
service OrdersReadService {
  rpc GetOpenOrders(.orders.v1.GetOpenOrdersRequest) returns (.orders.v1.GetOpenOrdersResponse);
  rpc GetOrderHistory(.orders.v1.GetOrderHistoryRequest) returns (.orders.v1.GetOrderHistoryResponse);
  rpc GetUserTrades(.orders.v1.GetUserTradesRequest) returns (.orders.v1.GetUserTradesResponse);
  rpc GetOrder(.orders.v1.GetOrderRequest) returns (.orders.v1.GetOrderResponse);
  rpc GetBatchReplaceStatus(.orders.v1.GetBatchReplaceStatusRequest) returns (.orders.v1.GetBatchReplaceStatusResponse);
}
```


## `polyester_api_options`

```
// polyester/api/options.proto  package=polyester.api
enum MFARequirement {
  MFA_UNSPECIFIED = 0;
  MFA_RECENT = 1;
  MFA_FRESH_STEP_UP = 2;
  MFA_CONDITIONAL = 3;
}
enum AuthenticationMethod {
  AUTH_UNSPECIFIED = 0;
  SESSION_TOKEN = 1;
  API_KEY = 2;
}
```


## `polyester_ratelimit_v1_types`

```
// polyester/ratelimit/v1/types.proto  package=polyester.ratelimit.v1
enum FailureReason {
  REASON_UNSPECIFIED = 0;
  QUOTA_EXCEEDED = 1;
  AUTHORITY_UNAVAILABLE = 2;
}
enum PolicyClass {
  CLASS_UNSPECIFIED = 0;
  AUTH_PUBLIC = 1;
  TRADING_PLACE = 2;
  TRADING_CANCEL = 3;
  TRADING_READ = 4;
  ACCOUNT_ADMIN = 5;
  PUBLIC_READ = 6;
  ACCOUNT_SECURITY = 7;
  DEPOSIT_CREATE = 8;
  INTERNAL_TRANSFER = 9;
  WITHDRAW_SUBMIT = 10;
  WITHDRAW_VALIDATE = 11;
  GUARD_SIGN = 12;
  SOCIAL_PROVIDER = 13;
}
enum LimiterScope {
  SCOPE_UNSPECIFIED = 0;
  CLIENT_IP = 1;
  API_KEY = 2;
  ACCOUNT = 3;
  SUBACCOUNT = 4;
  CONNECTION = 5;
  SERVICE = 6;
  REGION = 7;
  SYMBOL = 8;
  AUTH_SUBJECT = 9;
}
enum RefillModel {
  REFILL_UNSPECIFIED = 0;
  CONTINUOUS = 1;
  FIXED_WINDOW = 2;
  ROLLING_WINDOW = 3;
}
message RateLimitDetail {
  optional .polyester.ratelimit.v1.FailureReason reason = 1;
  optional 4 limit = 2;
  optional 4 remaining = 3;
  optional 4 retry_after_ms = 4;
  optional 4 policy_version = 5;
  optional 9 operation_id = 6;
  optional .polyester.ratelimit.v1.PolicyClass policy_class = 7;
  optional .polyester.ratelimit.v1.LimiterScope scope = 8;
  optional .polyester.ratelimit.v1.RefillModel refill_model = 9;
}
```


## `polyester_type_v1_u128`

```
// polyester/type/v1/u128.proto  package=polyester.type.v1
message U128 {
  optional 6 hi = 1;
  optional 6 lo = 2;
}
```


## `ratelimit_v1_ratelimit`

```
// ratelimit/v1/ratelimit.proto  package=ratelimit.v1
enum TradingRateLimitClass {
  TRADING_RATE_LIMIT_CLASS_UNSPECIFIED = 0;
  TRADING_RATE_LIMIT_CLASS_PLACE = 1;
  TRADING_RATE_LIMIT_CLASS_CANCEL = 2;
}
message TradingRateLimitRule {
  optional .ratelimit.v1.TradingRateLimitClass policy_class = 1;
  optional 13 vip_tier = 2;
  optional 4 quota_weight = 3;
  optional 4 period_ms = 4;
  optional 4 burst_weight = 5;
}
message GetRateLimitConfigRequest {
}
message GetRateLimitConfigResponse {
  optional 4 policy_version = 1;
  optional .google.protobuf.Timestamp effective_from = 2;
  repeated .ratelimit.v1.TradingRateLimitRule rules = 3;
}
message GetTradingRateLimitsRequest {
  optional 6 subaccount_id = 1;
}
message GetTradingRateLimitsResponse {
  optional 4 policy_version = 1;
  optional .google.protobuf.Timestamp effective_from = 2;
  repeated .ratelimit.v1.TradingRateLimitRule rules = 3;
  repeated .ratelimit.v1.TradingRateLimitRule api_key_rules = 4;
}
service RateLimitService {
  rpc GetRateLimitConfig(.ratelimit.v1.GetRateLimitConfigRequest) returns (.ratelimit.v1.GetRateLimitConfigResponse);
  rpc GetTradingRateLimits(.ratelimit.v1.GetTradingRateLimitsRequest) returns (.ratelimit.v1.GetTradingRateLimitsResponse);
}
```


## `transfer_v1_internal_transfer`

```
// transfer/v1/internal_transfer.proto  package=transfer.v1
enum ErrorCode {
  ERROR_CODE_UNSPECIFIED = 0;
  ERROR_CODE_INSUFFICIENT_FUNDS = 1;
  ERROR_CODE_INVALID_REQUEST = 2;
  ERROR_CODE_UNAUTHENTICATED = 3;
  ERROR_CODE_PERMISSION_DENIED = 4;
  ERROR_CODE_RATE_LIMIT_EXCEEDED = 5;
  ERROR_CODE_SERVICE_UNAVAILABLE = 6;
  ERROR_CODE_INTERNAL_ERROR = 7;
  ERROR_CODE_INVALID_SUBACCOUNT_ID = 8;
  ERROR_CODE_SUBACCOUNT_NOT_FOUND = 9;
  ERROR_CODE_SOURCE_ACCOUNT_INACTIVE = 10;
  ERROR_CODE_UNSUPPORTED_ASSET = 11;
  ERROR_CODE_INVALID_AMOUNT = 12;
  ERROR_CODE_INVALID_DESTINATION = 13;
  ERROR_CODE_DESTINATION_NOT_FOUND = 14;
  ERROR_CODE_DESTINATION_INACTIVE = 15;
  ERROR_CODE_SAME_SOURCE_DESTINATION = 16;
  ERROR_CODE_DESTINATION_NOT_WHITELISTED = 17;
  ERROR_CODE_SMART_ACCOUNT_UNAVAILABLE = 18;
  ERROR_CODE_STEP_UP_UNAVAILABLE = 19;
  ERROR_CODE_IDEMPOTENCY_CONFLICT = 20;
  ERROR_CODE_FUNDS_LOCK_CONFLICT = 21;
  ERROR_CODE_CAPITAL_VIEW_UNAVAILABLE = 22;
  ERROR_CODE_ACCOUNT_SHARD_UNAVAILABLE = 23;
  ERROR_CODE_POLICY_DENIED = 24;
  ERROR_CODE_FAILED_PRECONDITION = 25;
  ERROR_CODE_NOT_FOUND = 26;
  ERROR_CODE_CONFLICT = 27;
}
enum InternalTransferStatus {
  INTERNAL_TRANSFER_STATUS_UNSPECIFIED = 0;
  INTERNAL_TRANSFER_STATUS_ACCEPTED = 1;
  INTERNAL_TRANSFER_STATUS_REJECTED = 2;
  INTERNAL_TRANSFER_STATUS_FAILED = 3;
}
message CreateInternalTransferRequest {
  optional 6 subaccount_id = 1;
  optional 6 destination_account_id = 2;
  optional 6 destination_subaccount_id = 3;
  optional 9 destination_smart_account_address = 4;
  optional 13 asset_id = 5;
  optional .polyester.type.v1.U128 amount_e18 = 6;
  optional 9 idempotency_key = 7;
}
message ResolvedDestination {
  optional 9 root_account_public_id = 1;
  optional 9 subaccount_public_id = 2;
  optional 9 smart_account_address = 3;
}
message ErrorDetail {
  optional .transfer.v1.ErrorCode code = 1;
}
message CreateInternalTransferResponse {
  optional 9 request_id = 1;
  optional 9 transfer_id = 2;
  optional 4 accepted_at_ts_ns = 3;
  optional 13 asset_id = 4;
  optional 9 asset_code = 5;
  optional 9 u_asset_id = 6;
  optional .polyester.type.v1.U128 amount_e18 = 7;
  optional .transfer.v1.ResolvedDestination destination = 8;
  optional .transfer.v1.InternalTransferStatus status = 9;
}
service InternalTransferService {
  rpc CreateInternalTransfer(.transfer.v1.CreateInternalTransferRequest) returns (.transfer.v1.CreateInternalTransferResponse);
}
```


## `triggers_v1_triggers`

```
// triggers/v1/triggers.proto  package=triggers.v1
enum TriggerType {
  TRIGGER_TYPE_UNSPECIFIED = 0;
  STOP_LOSS = 1;
  TAKE_PROFIT = 2;
  TRAILING_STOP = 3;
  TWAP = 4;
  LADDER = 5;
}
enum TriggerStatus {
  STATUS_UNSPECIFIED = 0;
  STATUS_CREATED = 1;
  STATUS_ARMED = 2;
  STATUS_RUNNING = 3;
  STATUS_COMPLETED = 4;
  STATUS_CANCELED = 5;
  STATUS_FAILED = 6;
  STATUS_PAUSED = 7;
}
enum TriggerEventType {
  EVENT_UNSPECIFIED = 0;
  EVENT_FIRED = 1;
  EVENT_CANCELED = 2;
  EVENT_UPDATED = 3;
  EVENT_FAILED = 4;
  EVENT_ACTIVATED = 5;
}
enum TriggerCancelReason {
  TRIGGER_CANCEL_REASON_UNSPECIFIED = 0;
  TRIGGER_CANCEL_REASON_USER_REQUEST = 1;
  TRIGGER_CANCEL_REASON_OCO = 2;
  TRIGGER_CANCEL_REASON_PARENT_CANCELED_NO_FILL = 3;
  TRIGGER_CANCEL_REASON_MISSING_REASON_CODE = 998;
  TRIGGER_CANCEL_REASON_INTERNAL_ERROR = 999;
}
enum TriggerFailureReason {
  TRIGGER_FAILURE_REASON_UNSPECIFIED = 0;
  TRIGGER_FAILURE_REASON_UNKNOWN_SYMBOL = 1;
  TRIGGER_FAILURE_REASON_PAIR_DISABLED = 2;
  TRIGGER_FAILURE_REASON_MIN_NOTIONAL = 3;
  TRIGGER_FAILURE_REASON_TICK_SIZE = 4;
  TRIGGER_FAILURE_REASON_INSUFFICIENT_FUNDS = 5;
  TRIGGER_FAILURE_REASON_RISK_LIMIT = 6;
  TRIGGER_FAILURE_REASON_DUPLICATE_CLIENT_ID = 7;
  TRIGGER_FAILURE_REASON_MARKET_HALTED = 8;
  TRIGGER_FAILURE_REASON_ENGINE_BUSY = 9;
  TRIGGER_FAILURE_REASON_ACCOUNT_UNKNOWN = 10;
  TRIGGER_FAILURE_REASON_ORDER_UNKNOWN = 11;
  TRIGGER_FAILURE_REASON_POST_ONLY_CROSS = 12;
  TRIGGER_FAILURE_REASON_REDUCE_ONLY_BLOCKED = 13;
  TRIGGER_FAILURE_REASON_PRICE_BAND_VIOLATION = 14;
  TRIGGER_FAILURE_REASON_MARKET_CAP_VIOLATION = 15;
  TRIGGER_FAILURE_REASON_EMPTY_BOOK = 16;
  TRIGGER_FAILURE_REASON_FOK_INSUFFICIENT_LIQUIDITY = 17;
  TRIGGER_FAILURE_REASON_FEE_ASSET_NOT_ALLOWED = 18;
  TRIGGER_FAILURE_REASON_MARKET_PRICE_UNAVAILABLE = 19;
  TRIGGER_FAILURE_REASON_STALE_QUOTE = 20;
  TRIGGER_FAILURE_REASON_MIN_QUANTITY = 21;
  TRIGGER_FAILURE_REASON_STEP_SIZE = 22;
  TRIGGER_FAILURE_REASON_INVALID_SIZING = 23;
  TRIGGER_FAILURE_REASON_MAX_QUOTE_DEBIT_TOO_SMALL = 24;
  TRIGGER_FAILURE_REASON_FEE_CEILING_EXCEEDED = 25;
  TRIGGER_FAILURE_REASON_TRIGGER_PRICE_INVALID = 40;
  TRIGGER_FAILURE_REASON_TRIGGER_PRICE_SOURCE_UNSUPPORTED = 41;
  TRIGGER_FAILURE_REASON_TRAILING_DISTANCE_INVALID = 42;
  TRIGGER_FAILURE_REASON_MODIFICATION_REQUIRES_REPLACE = 43;
  TRIGGER_FAILURE_REASON_ORDER_ALREADY_TERMINAL = 44;
  TRIGGER_FAILURE_REASON_CONFLICT_IDEMPOTENCY_KEY_REUSE = 45;
  TRIGGER_FAILURE_REASON_RATE_LIMITED = 46;
  TRIGGER_FAILURE_REASON_POLICY_SPOT_TRADE_DENY = 47;
  TRIGGER_FAILURE_REASON_POLICY_MARKET_DENY = 48;
  TRIGGER_FAILURE_REASON_POLICY_MAX_NOTIONAL = 49;
  TRIGGER_FAILURE_REASON_POLICY_MAX_OPEN_ORDERS = 50;
  TRIGGER_FAILURE_REASON_POLICY_TRADING_HALTED = 51;
  TRIGGER_FAILURE_REASON_MISSING_REASON_CODE = 998;
  TRIGGER_FAILURE_REASON_INTERNAL_ERROR = 999;
}
enum LadderDistribution {
  LADDER_DISTRIBUTION_UNSPECIFIED = 0;
  LINEAR = 1;
  GEOMETRIC = 2;
  WEIGHTED_FAVORABLE = 3;
}
message TriggerMarketIoc {
}
message TriggerLimitGtc {
  optional 3 price_ticks = 1;
  optional 8 post_only = 2;
}
message TriggerLimitIoc {
  optional 3 price_ticks = 1;
}
message TriggerLimitFok {
  optional 3 price_ticks = 1;
}
message ConditionalChildExecution {
  optional .triggers.v1.TriggerMarketIoc market_ioc = 1;
  optional .triggers.v1.TriggerLimitGtc limit_gtc = 2;
  optional .triggers.v1.TriggerLimitIoc limit_ioc = 3;
  optional .triggers.v1.TriggerLimitFok limit_fok = 4;
}
message ConditionalTrigger {
  optional 3 trigger_price_ticks = 1;
  optional .orders.v1.Side side = 2;
  optional .triggers.v1.ConditionalChildExecution child = 3;
}
message TrailingStopTrigger {
  optional 3 trailing_distance_ticks = 1;
  optional 5 trailing_distance_bps = 2;
  optional 3 activation_price_ticks = 3;
  optional 3 max_slippage_ticks = 4;
  optional 5 max_slippage_bps = 5;
  optional .orders.v1.Side side = 6;
}
message TwapMarketIoc {
  optional 3 max_slippage_ticks = 1;
  optional 5 max_slippage_bps = 2;
}
message TwapLimitGtc {
  optional 3 price_ticks = 1;
}
message TwapTrigger {
  optional .orders.v1.Side side = 1;
  optional 3 duration_ms = 2;
  optional 3 slice_interval_ms = 3;
  optional .triggers.v1.TwapMarketIoc market_ioc = 4;
  optional .triggers.v1.TwapLimitGtc limit_gtc = 5;
}
message LadderTrigger {
  optional .orders.v1.Side side = 1;
  optional 3 price_min_ticks = 2;
  optional 3 price_max_ticks = 3;
  optional 5 levels = 4;
  optional 8 post_only = 5;
}
message TriggerIntent {
  optional 13 symbol_id = 1;
  optional 3 qty_scaled = 2;
  optional .orders.v1.FeeAsset fee_asset = 3;
  optional .orders.v1.SelfTradePreventionMode self_trade_prevention_mode = 4;
  optional 9 client_trigger_id = 5;
  optional .triggers.v1.ConditionalTrigger stop_loss = 10;
  optional .triggers.v1.ConditionalTrigger take_profit = 11;
  optional .triggers.v1.TrailingStopTrigger trailing_stop = 12;
  optional .triggers.v1.TwapTrigger twap = 13;
  optional .triggers.v1.LadderTrigger ladder = 14;
}
message CreateTriggerRequest {
  optional 6 subaccount_id = 1;
  optional .triggers.v1.TriggerIntent trigger = 2;
}
message CreateTriggerResponse {
  optional 6 trigger_id = 1;
  optional 9 client_trigger_id = 2;
  optional .google.protobuf.Timestamp accepted_at = 3;
  optional 4 accepted_at_ts_ns = 4;
}
message GetTriggerRequest {
  optional 6 trigger_id = 1;
  optional 6 subaccount_id = 2;
}
message GetTriggerResponse {
  optional .triggers.v1.Trigger trigger = 1;
}
message ListTriggersRequest {
  optional 6 subaccount_id = 1;
  optional 13 symbol_id = 2;
  repeated .triggers.v1.TriggerStatus status = 3;
  optional .triggers.v1.TriggerType trigger_type = 4;
  optional 6 parent_order_id = 5;
  optional 13 limit = 10;
  optional 9 page_token = 12;
}
message ListTriggersResponse {
  repeated .triggers.v1.Trigger triggers = 1;
  optional 9 next_page_token = 3;
}
message ListTriggerEventsRequest {
  optional 6 trigger_id = 1;
  optional 6 subaccount_id = 2;
  optional 13 limit = 3;
  optional .triggers.v1.TriggerEventType event_type = 4;
  optional 9 page_token = 5;
}
message TriggerEvent {
  optional 6 trigger_id = 1;
  optional 6 subaccount_id = 2;
  optional 13 symbol_id = 3;
  optional .triggers.v1.TriggerType trigger_type = 4;
  optional .triggers.v1.TriggerEventType event_type = 5;
  optional 4 ts_ns = 10;
  optional 5 child_seq = 11;
  optional 6 child_order_id = 12;
  optional 3 fire_price_ticks = 13;
  optional .triggers.v1.TriggerCancelReason cancel_reason = 20;
  optional .triggers.v1.TriggerFailureReason failure_reason = 21;
}
message ListTriggerEventsResponse {
  repeated .triggers.v1.TriggerEvent events = 1;
  optional 9 next_page_token = 3;
}
message CancelTriggerRequest {
  optional 6 trigger_id = 1;
  optional 6 subaccount_id = 2;
}
message CancelTriggerResponse {
  optional 6 trigger_id = 1;
  optional .triggers.v1.TriggerStatus status = 2;
  optional .google.protobuf.Timestamp ts = 3;
  optional 4 ts_ns = 4;
}
message ModifyTriggerRequest {
  optional 6 trigger_id = 1;
  optional 6 subaccount_id = 2;
  optional 13 symbol_id = 3;
  optional 3 trigger_price_ticks = 10;
  optional 3 limit_price_ticks = 11;
  optional 3 trailing_distance_ticks = 12;
  optional 5 trailing_distance_bps = 13;
  optional 3 activation_price_ticks = 14;
  optional 3 max_slippage_ticks = 15;
  optional 5 max_slippage_bps = 16;
}
message ModifyTriggerResponse {
  optional 6 trigger_id = 1;
  optional .triggers.v1.TriggerStatus status = 2;
  optional .google.protobuf.Timestamp ts = 3;
  optional 4 ts_ns = 4;
}
message PauseTriggerRequest {
  optional 6 trigger_id = 1;
  optional 6 subaccount_id = 2;
}
message PauseTriggerResponse {
  optional 6 trigger_id = 1;
  optional .triggers.v1.TriggerStatus status = 2;
  optional .google.protobuf.Timestamp ts = 3;
  optional 4 ts_ns = 4;
}
message ResumeTriggerRequest {
  optional 6 trigger_id = 1;
  optional 6 subaccount_id = 2;
  optional 13 symbol_id = 3;
}
message ResumeTriggerResponse {
  optional 6 trigger_id = 1;
  optional .triggers.v1.TriggerStatus status = 2;
  optional .google.protobuf.Timestamp ts = 3;
  optional 4 ts_ns = 4;
}
message StopDetails {
  optional 3 trigger_price_ticks = 1;
  optional .orders.v1.TriggerPriceSource trigger_price_source = 2;
  optional .orders.v1.TriggerDirection trigger_direction = 3;
}
message TrailingDetails {
  optional 3 trailing_distance_ticks = 1;
  optional 3 activation_price_ticks = 2;
  optional 3 peak_price_ticks = 3;
  optional 3 trough_price_ticks = 4;
  optional 5 trailing_distance_bps = 5;
  optional 3 max_slippage_ticks = 6;
  optional 5 max_slippage_bps = 7;
  optional .orders.v1.TriggerPriceSource trigger_price_source = 8;
  optional .orders.v1.TriggerDirection trigger_direction = 9;
  optional 3 trigger_price_ticks = 10;
}
message TwapDetails {
  optional 3 twap_duration_ms = 1;
  optional 3 twap_slice_interval_ms = 2;
  optional 5 slice_idx = 4;
  optional 5 slice_count = 5;
  optional 3 executed_qty_scaled = 6;
}
message LadderDetails {
  optional 3 ladder_price_min_ticks = 1;
  optional 3 ladder_price_max_ticks = 2;
  optional 5 ladder_levels = 3;
  optional .triggers.v1.LadderDistribution ladder_distribution = 4;
  optional 3 executed_qty_scaled = 5;
  optional 5 executed_levels = 6;
}
message Trigger {
  optional 6 trigger_id = 1;
  optional 6 subaccount_id = 2;
  optional 13 symbol_id = 3;
  optional .triggers.v1.TriggerStatus status = 5;
  optional 6 parent_order_id = 6;
  optional .triggers.v1.TriggerCancelReason cancel_reason = 7;
  optional .triggers.v1.TriggerFailureReason failure_reason = 8;
  optional 3 qty_scaled = 20;
  optional .orders.v1.FeeAsset fee_asset = 21;
  optional .orders.v1.SelfTradePreventionMode self_trade_prevention_mode = 22;
  optional .triggers.v1.ConditionalTrigger stop_loss = 30;
  optional .triggers.v1.ConditionalTrigger take_profit = 31;
  optional .triggers.v1.TrailingStopTrigger trailing_stop = 32;
  optional .triggers.v1.TwapTrigger twap = 33;
  optional .triggers.v1.LadderTrigger ladder = 34;
  optional .triggers.v1.StopDetails stop = 100;
  optional .triggers.v1.TrailingDetails trailing = 101;
  optional .triggers.v1.TwapDetails twap_state = 102;
  optional .triggers.v1.LadderDetails ladder_state = 103;
  optional 9 client_trigger_id = 60;
  optional .google.protobuf.Timestamp created_at = 61;
  optional .google.protobuf.Timestamp updated_at = 62;
  optional .google.protobuf.Timestamp armed_at = 63;
  optional .google.protobuf.Timestamp completed_at = 64;
}
service TriggersService {
  rpc CreateTrigger(.triggers.v1.CreateTriggerRequest) returns (.triggers.v1.CreateTriggerResponse);
  rpc GetTrigger(.triggers.v1.GetTriggerRequest) returns (.triggers.v1.GetTriggerResponse);
  rpc ListTriggers(.triggers.v1.ListTriggersRequest) returns (.triggers.v1.ListTriggersResponse);
  rpc ListTriggerEvents(.triggers.v1.ListTriggerEventsRequest) returns (.triggers.v1.ListTriggerEventsResponse);
  rpc CancelTrigger(.triggers.v1.CancelTriggerRequest) returns (.triggers.v1.CancelTriggerResponse);
  rpc ModifyTrigger(.triggers.v1.ModifyTriggerRequest) returns (.triggers.v1.ModifyTriggerResponse);
  rpc PauseTrigger(.triggers.v1.PauseTriggerRequest) returns (.triggers.v1.PauseTriggerResponse);
  rpc ResumeTrigger(.triggers.v1.ResumeTriggerRequest) returns (.triggers.v1.ResumeTriggerResponse);
}
```


## `vip_v1_vip`

```
// vip/v1/vip.proto  package=vip.v1
message VIPTier {
  optional 13 tier = 1;
  optional 9 volume_threshold_usd = 2;
  optional 9 aop_threshold_usd = 3;
  optional 9 maker_fee_rate_percent = 4;
  optional 9 taker_fee_rate_percent = 5;
}
message ListVIPTiersRequest {
}
message ListVIPTiersResponse {
  optional 4 policy_version = 1;
  optional .google.protobuf.Timestamp effective_from = 2;
  optional 13 retention_threshold_bp = 3;
  repeated .vip.v1.VIPTier tiers = 4;
}
message NextVIPTierThresholds {
  optional 13 tier = 1;
  optional 9 volume_threshold_usd = 2;
  optional 9 aop_threshold_usd = 3;
}
message GetVIPStatusRequest {
}
message GetVIPStatusResponse {
  optional 13 tier = 1;
  optional 13 volume_tier = 2;
  optional 13 aop_tier = 3;
  optional 9 settled_volume_30d_usd = 4;
  optional 9 average_aop_30d_usd = 5;
  optional 4 policy_version = 6;
  optional .google.protobuf.Timestamp policy_effective_from = 7;
  optional .google.protobuf.Timestamp effective_from = 8;
  optional .google.protobuf.Timestamp evaluated_at = 9;
  optional .google.protobuf.Timestamp metrics_as_of = 10;
  optional .vip.v1.NextVIPTierThresholds next_tier_thresholds = 11;
}
service VIPService {
  rpc ListVIPTiers(.vip.v1.ListVIPTiersRequest) returns (.vip.v1.ListVIPTiersResponse);
  rpc GetVIPStatus(.vip.v1.GetVIPStatusRequest) returns (.vip.v1.GetVIPStatusResponse);
}
```
