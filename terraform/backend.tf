terraform {
  backend "gcs" {
    bucket = "seu-bucket-para-terraform-state"
    prefix = "terraform/state"
  }
}
