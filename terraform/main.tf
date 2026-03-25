resource "azurerm_resource_group" "civicpulserg" {
  name     = "civicpulserg24"
  location = "southafricanorth"
}

resource "azurerm_storage_account" "civicpulse" {
  name                     = "civicpulse22456"
  resource_group_name      = azurerm_resource_group.civicpulserg.name
  location                 = azurerm_resource_group.civicpulserg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  tags = {
    environment = "staging"
  }
}

resource "azurerm_storage_container" "rawcontainer" {
  name                  = "bronze"
  storage_account_name  = azurerm_storage_account.civicpulse.name
  container_access_type = "private"
}


resource "azurerm_storage_container" "silvercontainer" {
  name                  = "silver"
  storage_account_name  = azurerm_storage_account.civicpulse.name
  container_access_type = "private"
  depends_on            = [azurerm_storage_account.civicpulse]
}

// postgresql server

resource "azurerm_postgresql_flexible_server" "civiclogicserver" {
  name                          = var.postgres_server
  resource_group_name           = var.resource_group_name
  location                      = var.location
  version                       = "15"
  public_network_access_enabled = true
  administrator_login           = var.db_admin_login
  administrator_password        = var.db_admin_pass
  zone                          = "1"

  storage_mb   = 32768
  storage_tier = "P30"

  sku_name    = "GP_Standard_D4s_v3"
  create_mode = "Default"

  authentication {
    password_auth_enabled = true
  }

  depends_on = [azurerm_resource_group.civicpulserg]

}

resource "azurerm_postgresql_flexible_server_database" "civiclogicdb" {
  name      = "civic_logic_db"
  server_id = azurerm_postgresql_flexible_server.civiclogicserver.id
  collation = "en_US.utf8"
  charset   = "utf8"

  # prevent the possibility of accidental data loss
  lifecycle {
    prevent_destroy = false
  }
}
 resource "azurerm_data_factory" "civiclogic" {
  name                = "civiclogic25"
  location            = azurerm_resource_group.civicpulserg.location
  resource_group_name = azurerm_resource_group.civicpulserg.name
}


resource "azurerm_data_factory_linked_service_azure_blob_storage" "civiclogicstoragels" {
  name              = "civiclogic_blob_ls"
  data_factory_id   = azurerm_data_factory.civiclogic.id
  connection_string = azurerm_storage_account.civicpulse.primary_connection_string
}

module "data_factory_blob_storage" {
  source              = "./data_factory_blob_storage"
  data_factory_id     = azurerm_data_factory.civiclogic.id
  linked_service_name = azurerm_data_factory_linked_service_azure_blob_storage.civiclogicstoragels.name

}