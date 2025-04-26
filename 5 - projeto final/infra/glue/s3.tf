resource "aws_s3_bucket" "bucket_source_code" {
  bucket = "walter-araujo-bucket-source-code"
}

resource "aws_s3_bucket_object" "glue_job_main" {
  bucket = aws_s3_bucket.bucket_source_code.bucket
  key    = "etl_sor/main.py"
  content = file("${path.module}/../../app/glue/etl_sor/main.py")
}

resource "aws_s3_bucket_object" "glue_job_ingestao_s3" {
  bucket = aws_s3_bucket.bucket_source_code.bucket
  key    = "etl_sor/ingestao_s3.py"
  content = file("${path.module}/../../app/glue/etl_sor/ingestao_s3.py")
}