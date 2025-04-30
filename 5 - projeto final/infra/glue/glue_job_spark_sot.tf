resource "aws_glue_job" "glue_job_spark_sot" {
    name = "walter.araujo.glue_job_spark_sot"
    role_arn = var.role_arn

    worker_type = "G.1X"
    number_of_workers = 2
    glue_version = "5.0"

    default_arguments = {
    "--enable-glue-datacatalog" = "true"
    }

    command {
        name = "glueetl"
        script_location = "s3://${aws_s3_bucket.bucket_source_code.bucket}/etl_sot/ingestao_sot.py"
        python_version = "3"
    }

    depends_on = [ aws_s3_bucket.bucket_source_code ]
}