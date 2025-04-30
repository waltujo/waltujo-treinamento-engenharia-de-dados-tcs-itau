resource "aws_sfn_state_machine" "sfn_walter_araujo_ingestao_dados" {
    name = "sfn_walter_araujo_ingestao_dados"
    role_arn = var.role_arn_walter
    definition = file("${path.module}../../../app/stepFunctions/ingestao.json")
}

resource "aws_cloudwatch_event_rule" "eventbridge_sfn_walter_araujo_ingestao_dados" {
    name = "eventbridge_sfn_walter_araujo_ingestao_dados"
    description = "Agendar o fluxo de ingestão de dados a cada 1 hora"
    schedule_expression = "cron(0/10 * ? * MON-FRI *)" #"cron(0 0 ? * MON-FRI *)"

    depends_on = [ aws_sfn_state_machine.sfn_walter_araujo_ingestao_dados ]
}

resource "aws_cloudwatch_event_target" "eventbridge_sfn_walter_araujo_ingestao_dados" {
    rule = aws_cloudwatch_event_rule.eventbridge_sfn_walter_araujo_ingestao_dados.name
    arn = aws_sfn_state_machine.sfn_walter_araujo_ingestao_dados.arn
    role_arn = var.role_arn_walter

    depends_on = [ aws_cloudwatch_event_rule.eventbridge_sfn_walter_araujo_ingestao_dados ]
}