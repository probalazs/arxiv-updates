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
    "user:allUsers"
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
    "user:allUsers"
  ]
}

resource "google_service_account" "test" {
  account_id = "arxiv-updates-test"
}

data "google_cloudfunctions_function" "arxiv_updates" {
  name = "arxiv-updates"
}

resource "google_cloud_scheduler_job" "check_for_updates" {
  name      = "check-for-updates"
  schedule  = "30 4 * * *"
  time_zone = "Europe/Budapest"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = data.google_cloudfunctions_function.arxiv_updates.https_trigger_url
    body        = "{\"bucket\":\"${google_storage_bucket.releases.name}\",\"rss\":\"http://export.arxiv.org/rss/cs.AI\"}"
  }
}
