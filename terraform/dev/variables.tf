variable "project_name" {
  description = "Project name"
  default     = "project-name"
}

variable "source_bucket_name" {
  description = "Source bucket name"
  default     = "source-bucket-name"
}

variable "destination_bucket_name" {
  description = "Destination bucket name"
  default     = "destination-bucket-name"
}

resource "null_resource" "run_python_script" {
  provisioner "local-exec" {
    command = "python processing_img.py ${var.source_bucket_name} ${var.destination_bucket_name}"
  }
}
