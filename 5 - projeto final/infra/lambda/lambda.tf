# Criação do arquivo ZIP
data "archive_file" "zip_python_code" {
  type        = "zip"
  source_dir  = "${path.module}"  # Diretório onde está o código Python
  output_path = "${path.module}/lambda_ingestao.zip"  # Saída do arquivo ZIP
}

# Criação da função Lambda
resource "aws_lambda_function" "my_lambda" {
  filename         = data.archive_file.zip_python_code.output_path  # Referência ao caminho do arquivo ZIP
  function_name    = "walter_lambda_ingestion"
  role             = var.role_arn
  handler          = "lambda_ingestao.lambda_handler"  # Nome do arquivo (sem extensão) + função
  runtime          = "python3.11"
  source_code_hash = filebase64sha256(data.archive_file.zip_python_code.output_path)  # Hash para detectar alterações no código
}
