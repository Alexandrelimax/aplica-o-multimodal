variable "project_id" {
  type        = string
  description = "ID do projeto GCP"
}

variable "region" {
  type        = string
  description = "Região para os recursos"
  default     = "us-central1"
}

variable "zone" {
  type        = string
  description = "Nome do repositório GitHub"
}

variable "github_owner" {
  type        = string
  description = "Dono do repositório GitHub"
}

variable "github_repo" {
  type        = string
  description = "Nome do repositório GitHub"
}

variable "repository_id" {
  type        = string
  description = "Nome do repositório GitHub"
}

variable "cloud_run_name" {
  type        = string
  description = "Nome do repositório GitHub"
}

variable "cloud_build_name" {
  type        = string
  description = "Nome do repositório GitHub"
}