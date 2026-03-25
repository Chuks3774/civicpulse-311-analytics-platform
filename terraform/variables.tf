variable "location" {
  type    = string
  default = "southafricanorth"
}

variable "resource_group_name" {
  type    = string
  default = "civicpulserg24"
}

variable "storage_account" {
  type    = string
  default = "civicstorageacct22"
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
  default = "civiclogicserver33"
}