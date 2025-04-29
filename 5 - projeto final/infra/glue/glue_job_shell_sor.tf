resource "aws_glue_job" "glue_job_shell" {
    name = "walter.araujo.glue_job_shell"
    role_arn = "arn:aws:iam::471112636571:role/guilherme.magalhaes-role-glue"

    max_capacity = 1.0
    
    default_arguments = {
      "library-set" = "analytics"
    }

    command {
        name = "pythonshell"
        script_location = "s3://${aws_s3_bucket.bucket_source_code.bucket}/etl_sor/ingestao_s3.py"
        python_version = "3.9"
    }

    depends_on = [ aws_s3_bucket.bucket_source_code ]
}