variable "location" {
  type    = string
  default = "southafricanorth"
}

variable "resource_group_name" {
  type    = string
  default = "civicpulserg"
}

variable "storage_account" {
  type    = string
  default = "civicstorageacct"
}

variable "db_admin_login" {
  type      = string
  sensitive = true
}

variable "db_admin_pass" {
  type      = string
  sensitive = true
}

variable "postgres_server" {
  type    = string
  default = "civiclogicserver3"
}