
resource "aws_glue_catalog_table" "tb_sot_financeira" {
  name = "sot_financeira"
  database_name = aws_glue_catalog_database.walteraraujo_database_sot.name
  table_type = "EXTERNAL_TABLE"

  parameters = {
    "classification" = "parquet"
    "compressionType" = "snappy"
  }

    storage_descriptor {
        location = "s3://walter-araujo-bucket-exemplo-sot/sot_financeira"
        input_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
        output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

        ser_de_info {
        serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
        }

        columns {
            name = "identificador_unico"
            type = "string"
        }

        columns {
            name = "transacao_id"
            type = "int"
        }

        columns {
            name = "conta_id"
            type = "int"
        }

        columns {
            name = "categoria_id"
            type = "int"
        }

        columns {
            name = "transacao_data"
            type = "timestamp"
        }

        columns {
            name = "transacao_ano"
            type = "int"
        }

        columns {
            name = "transacao_mes"
            type = "int"
        }

        columns {
            name = "transacao_dia"
            type = "int"
        }

        columns {
            name = "transacao_descricao"
            type = "string"
        }

        columns {
            name = "transacao_valor"
            type = "string"
        }

        columns {
            name = "transacao_data_criacao"
            type = "string"
        }

        columns {
            name = "conta_nome"
            type = "string"
        }

        columns {
            name = "conta_descricao"
            type = "string"
        }

        columns {
            name = "categoria_nome"
            type = "string"
        }

        columns {
            name = "categoria_tipo"
            type = "string"
        }

        columns {
            name = "taxa_juros_referencia"
            type = "string"
        }

        columns {
            name = "taxa_juros_porcentagem"
            type = "string"
        }
    }

    partition_keys {
        name = "data_ingestao"
        type = "string"
    }

    depends_on = [aws_glue_catalog_database.walteraraujo_database_sot]
}