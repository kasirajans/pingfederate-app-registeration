# PingFederate App Registration

This repository contains Terraform configurations for registering applications with PingFederate. The configurations are organized by region (US and EU) and environment (Dev, Prod).

## Folder Structure

```
/Users/kraaj/Project/Public/pingfederate-app-registeration/
├── US/
│   ├── Dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── backend.tf
│   │   ├── us.dev.tfvars
│   ├── Prod/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── backend.tf
│   │   ├── us.prod.tfvars
├── EU/
│   ├── Dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── backend.tf
│   │   ├── eu.dev.tfvars
│   ├── Prod/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── backend.tf
│   │   ├── eu.prod.tfvars
├── scripts/
│   ├── read_yaml.py
├── README.md
```

## Prerequisites

- Terraform >= 1.1
- Python (for running the `read_yaml.py` script)

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-repo/pingfederate-app-registeration.git
    cd pingfederate-app-registeration
    ```

2. **Navigate to the desired environment:**

    ```sh
    cd US/Dev
    ```

3. **Initialize Terraform:**

    ```sh
    terraform init
    ```

## Plan and Apply

### US Region

#### Dev Environment

1. **Navigate to the US Dev folder:**

    ```sh
    cd US/Dev
    ```

2. **Create a plan:**

    ```sh
    terraform plan -var-file="us.dev.tfvars"
    ```

3. **Apply the plan:**

    ```sh
    terraform apply -var-file="us.dev.tfvars"
    ```

#### Prod Environment

1. **Navigate to the US Prod folder:**

    ```sh
    cd US/Prod
    ```

2. **Create a plan:**

    ```sh
    terraform plan -var-file="us.prod.tfvars"
    ```

3. **Apply the plan:**

    ```sh
    terraform apply -var-file="us.prod.tfvars"
    ```

### EU Region

#### Dev Environment

1. **Navigate to the EU Dev folder:**

    ```sh
    cd EU/Dev
    ```

2. **Create a plan:**

    ```sh
    terraform plan -var-file="eu.dev.tfvars"
    ```

3. **Apply the plan:**

    ```sh
    terraform apply -var-file="eu.dev.tfvars"
    ```

#### Prod Environment

1. **Navigate to the EU Prod folder:**

    ```sh
    cd EU/Prod
    ```

2. **Create a plan:**

    ```sh
    terraform plan -var-file="eu.prod.tfvars"
    ```

3. **Apply the plan:**

    ```sh
    terraform apply -var-file="eu.prod.tfvars"
    ```

## Backend Configuration

Each environment has its own backend configuration to store the Terraform state files separately. The backend configuration is defined in the `backend.tf` file within each environment folder.

Example `backend.tf` for US Dev environment:

```tf
terraform {
  backend "local" {
    path = "${path.module}/us.dev/terraform.tfstate"
  }
}
```

## Variables

Common variables are defined in the `variables.tf` file. Environment-specific values are provided in the respective `.tfvars` files.

Example `variables.tf`:

```tf
variable "env" {
  description = "The environment (e.g., US/Prod)"
  type        = string
}
variable "yaml_file" {
  description = "The name of the YAML file"
  type        = string
}
variable "PINGFEDERATE_AUD" {
  type = string
}
```

## Scripts

The `scripts` folder contains helper scripts such as `read_yaml.py` for reading YAML files.

## Contact

For any issues or questions, please contact the business owner or technical owner as specified in the `appConfig.yaml` files.

## Sample `us.dev.tfvars` File

Below is an example of a `us.dev.tfvars` file with environment-specific variables:

```hcl
HTTP_CLI_ARGS="-tls-skip-verify"
PINGFEDERATE_ISSUER="https://idp.pingfed.kraaj.local"
PINGFEDERATE_AUD="api://kraaj.local"
PINGFEDERATE_PROVIDER_PRODUCT_VERSION="12.1"
PINGFEDERATE_PROVIDER_HTTPS_HOST="https://idp.pingfed.kraaj.local:9999"
PINGFEDERATE_PROVIDER_ADMIN_API_PATH="/pf-admin-api/v1"
PINGFEDERATE_PROVIDER_USERNAME=<password>
PINGFEDERATE_LDAP_DATASTORE="LDAP-DA8F73BDA44EDFBFF71DADA73D41CF1FAC649E4D"
PINGDIRECTROY_REST_API_URL="https://pingdir.kraaj.local:1443"
PINGDIRECTROY_USERNAME=<password>
PINGDIRECTROY_ROOTDN="dc=kraaj,dc=local"
machine_base_dn_value="ou=Machines,dc=kraaj,dc=local"
```
