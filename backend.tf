terraform {
  backend "local" {
    path = "${path.module}/${var.env}/terraform.tfstate"
  }
}
