resource "google_artifact_registry_repository" "docker_repo" {
  provider      = google
  format        = "DOCKER"
  location      = var.region
  repository_id = var.repository_id
}

resource "google_cloud_run_service" "app_service" {
  name     = var.cloud_run_name
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/app-image"
        ports {
          container_port = 8080
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloudbuild_trigger" "ci_cd_trigger" {
  name = "trigger-pipeline"

  github {
    owner = var.github_owner
    name  = var.github_repo

    push {
      branch = "^main$"
    }
  }

  filename = "cloudbuild.yaml"
}
