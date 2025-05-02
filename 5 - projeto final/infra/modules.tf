module "tables" {
  source = "./tables"
}

module "glue_job" {
  source = "./glue"
  role_arn = var.role_arn_walter
}

module "IAM" {
  source = "./iam"
}

module "lambda" {
  source = "./lambda"
  role_arn = var.role_arn_walter
}