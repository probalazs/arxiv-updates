terraform {
  backend "gcs" {
    bucket = "arxiv_updates_tfstate"
    prefix = "terraform/state"
  }
}

terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  impersonate_service_account = "terraform@clean-fin-392913.iam.gserviceaccount.com"
  project                     = "clean-fin-392913"
  region                      = "europe-west3"
}

resource "google_service_account" "application" {
  account_id = "arxiv-updates-application"
}

resource "google_storage_bucket" "releases" {
  name          = "arxiv-updates-releases"
  location      = "europe-west3"
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_binding" "releases_object_viewer" {
  depends_on = [google_storage_bucket.releases]
  bucket     = google_storage_bucket.releases.name
  role       = "roles/storage.objectViewer"
  members = [
    "allUsers"
  ]
}

resource "google_storage_bucket_iam_binding" "object_creator" {
  depends_on = [google_service_account.application, google_storage_bucket.releases]
  bucket     = google_storage_bucket.releases.name
  role       = "roles/storage.objectCreator"
  members = [
    google_service_account.application.member
  ]
}

resource "google_storage_bucket_iam_binding" "object_viewer" {
  depends_on = [google_service_account.application, google_storage_bucket.releases]
  bucket     = google_storage_bucket.releases.name
  role       = "roles/storage.objectViewer"
  members = [
    google_service_account.application.member
  ]
}

resource "google_service_account" "test" {
  account_id = "test-application"
}

resource "google_storage_bucket" "test" {
  name          = "arxiv-updates-test"
  location      = "europe-west3"
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket_iam_binding" "object_admin" {
  depends_on = [google_service_account.test, google_storage_bucket.test]
  bucket     = google_storage_bucket.test.name
  role       = "roles/storage.objectAdmin"
  members = [
    google_service_account.test.member
  ]
}

resource "google_storage_bucket" "static-site" {
  name          = "arxiv-updates-static-site"
  location      = "europe-west3"
  force_destroy = true

  uniform_bucket_level_access = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }
}

resource "google_storage_bucket_iam_binding" "static_site_object_viewer" {
  depends_on = [google_storage_bucket.static-site]
  bucket     = google_storage_bucket.static-site.name
  role       = "roles/storage.objectViewer"
  members = [
    "allUsers"
  ]
}
