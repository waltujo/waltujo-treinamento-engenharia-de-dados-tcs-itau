resource "aws_glue_catalog_table" "tb_categorias" {
  name = "categorias"
  database_name = aws_glue_catalog_database.walteraraujo_database_sor.name
  table_type = "EXTERNAL_TABLE"

  parameters = {
    "classification" = "parquet"
    "compressionType" = "snappy"
  }

    storage_descriptor {
        location = "s3://walter-araujo-bucket-exemplo/categorias"
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
            name = "nome"
            type = "string"
        }

         columns {
            name = "tipo"
            type = "string"
        }
    }

    partition_keys {
        name = "data_ingestao"
        type = "string"
    }

    depends_on = [aws_glue_catalog_database.walteraraujo_database_sor]
}