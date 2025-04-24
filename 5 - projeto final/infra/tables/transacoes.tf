
resource "aws_glue_catalog_table" "tb_transacoes" {
  name = "transacoes"
  database_name = aws_glue_catalog_database.walteraraujo_database_sor.name
  table_type = "EXTERNAL_TABLE"

  parameters = {
    "classification" = "parquet"
    "compressionType" = "snappy"
  }

    storage_descriptor {
        location = "s3://walter-araujo-bucket-exemplo/transacoes"
        input_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
        output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

        ser_de_info {
        serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
        }

        columns {
            name = "id"
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
            name = "data"
            type = "string"
        }

        columns {
            name = "descricao"
            type = "string"
        }

        columns {
            name = "valor"
            type = "string"
        }

        columns {
            name = "data_criacao"
            type = "string"
        }
    }

    partition_keys {
        name = "data_ingestao"
        type = "string"
    }

    depends_on = [aws_glue_catalog_database.walteraraujo_database_sor]
}