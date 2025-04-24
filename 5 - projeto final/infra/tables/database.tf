resource "aws_glue_catalog_database" "walteraraujo_database_sor" {
  name = "walter_araujo_database_sor"
  depends_on = [ aws_s3_bucket.bucket_exemplo ]
}

resource "aws_glue_catalog_database" "walteraraujo_database_sot" {
  name = "walter_araujo_database_sot"
  depends_on = [ aws_s3_bucket.bucket_exemplo_sot ]
}