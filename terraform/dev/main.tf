provider "google" {
  project = var.project_id
  region  = var.region
}

# 使用するサービスアカウント
resource "google_service_account" "func_service_account" {
  account_id   = "gcf-sa"
  display_name = "gcf-sa"
  project      = var.project_id
  description  = "Cloud Functions が使用するサービスアカウント"
}

# サービスアカウントに必要な権限を付与
resource "google_project_iam_member" "binding_cloudfunctions_serviceagent" {
  project = var.project_id
  role    = "roles/cloudfunctions.serviceAgent"
  member  = "serviceAccount:${google_service_account.func_service_account.email}"
}

resource "google_project_iam_member" "binding_cloudrun_serviceagent" {
  project = var.project_id
  role    = "roles/run.serviceAgent"
  member  = "serviceAccount:${google_service_account.func_service_account.email}"
}

resource "google_project_iam_member" "binding_secretmanager_secretaccessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.func_service_account.email}"
}

resource "google_project_iam_member" "binding_storage_objectadmin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.func_service_account.email}"
}

#### Cloud Functions 関連（デプロイ用 zip ファイルの作成）
# Cloud Functions デプロイ用にソースコード zip ファイルを作成
data "archive_file" "source_file_zip" {
  type        = "zip"
  source_dir  = "../../src"
  output_path = "../../${var.function_name}-${var.env}.zip"
}

#### Cloud Functions 関連（デプロイ用 GCS バケット、オブジェクトの作成）
# Cloud Functions ソースコードを格納する GCS バケットの作成
resource "google_storage_bucket" "src_cloud_functions" {
  name     = "${var.function_name}_functions_src"
  project  = var.project_id
  location = var.region
}
# Cloud Functions ソースコード GCS オブジェクトの作成
resource "google_storage_bucket_object" "source_object_zip" {
  name   = "${var.env}/${var.function_name}_${data.archive_file.source_file_zip.output_md5}.zip"
  bucket = google_storage_bucket.src_cloud_functions.name
  source = data.archive_file.source_file_zip.output_path
}


#### Cloud Functions 関連（各関数をデプロイ）
# アプリケーション を Cloud Functions へデプロイ
resource "google_cloudfunctions2_function" "function" {
  name        = "${var.function_name}-${var.env}"
  location    = var.region
  description = "deploy ${var.function_name}-${var.env}"

  # ソースコード、言語、エントリーポイントを指定
  build_config {
    runtime     = "python310"
    entry_point = "main"
    source {
      storage_source {
        bucket = google_storage_bucket.src_cloud_functions.name
        object = google_storage_bucket_object.source_object_zip.name
      }
    }
  }
  # 基本スペックの設定
  service_config {
    max_instance_count    = 10
    available_memory      = "512Mi"
    timeout_seconds       = 120
    service_account_email = google_service_account.func_service_account.email
    environment_variables = {
      SOURCE_BUCKET_NAME      = var.source_bucket_name
      DESTINATION_BUCKET_NAME = var.destination_bucket_name
    }
  }
}
