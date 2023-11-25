variable "project_id" {
  description = "GCP project id"
  default     = "quick-brief-406217"
}

variable "region" {
  description = "region"
  default     = "asia-northeast1"
}

variable "function_name" {
  description = "my function name"
  default     = "convert_img_to_text"
}

variable "env" {
  description = "select environment"
  default     = "dev"
}

variable "source_bucket_name" {
  description = "Source bucket name"
  default     = "test_book_image"
}

variable "destination_bucket_name" {
  description = "Destination bucket name"
  default     = "test_output_text"
}
