terraform {

  // 1. バックエンドをローカルで管理する場合の記述
  #   backend "local" {}

  // 2. バックエンドをGCSで管理する場合の記述 //

  backend "gcs" {
    # バックエンド tfstate ファイルを格納するバケットを指定
    bucket = "quick-brief-terraform-backend"
    prefix = "quick-brief/state/dev"
  }
}
resource "google_storage_bucket" "terraform_state" {
  # バックエンド tfstate ファイルを格納するバケットを指定
  name     = "quick-brief-terraform-backend"
  location = var.region
  # バージョン管理を有効にする
  versioning {
    enabled = true
  }
  # ライフサイクルで過去20バージョンを保存する
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      num_newer_versions = 10
    }
  }
}
