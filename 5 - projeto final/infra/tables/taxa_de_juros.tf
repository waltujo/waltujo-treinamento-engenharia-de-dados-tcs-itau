resource "aws_glue_catalog_table" "interest_rate_table" {
    name = "interest_rate"
    database_name = aws_glue_catalog_database.walteraraujo_database_sor.name
    table_type = "EXTERNAL_TABLE"

    storage_descriptor {
        location = "s3://walter-araujo-bucket-exemplo/interest_rate"
        input_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
        output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

        ser_de_info {
            serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
            }
        
        columns {
            name = "data_referencia"
            type = "string"
        }

        columns {
            name = "porcentagem"
            type = "string"
        }
    }

    partition_keys {
        name = "data_ingestao"
        type = "string"
    }

    depends_on = [aws_glue_catalog_database.walteraraujo_database_sor]
}