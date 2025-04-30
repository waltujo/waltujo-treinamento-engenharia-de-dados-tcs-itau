resource "aws_iam_role" "aws_iam_role_glue" {
    name = "walter_araujo_role_glue"
    assume_role_policy = file("${path.module}/assume_policy.json")
}

resource "aws_iam_policy" "aws_iam_policy_glue" {
    name        = "walter_araujo_policy_glue"
    description = "IAM policy for Glue jobs"
    policy      = file("${path.module}/policy.json")
}

resource "aws_iam_role_policy_attachment" "aws_iam_role_policy_attachment_glue" {
    role       = aws_iam_role.aws_iam_role_glue.name
    policy_arn = aws_iam_policy.aws_iam_policy_glue.arn
}