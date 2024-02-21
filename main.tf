# Add TF Data Bucket to S3
resource "aws_s3_bucket" "data_bucket" {
  bucket = var.data_bucket
}

# Add Data To S3 Bucket
resource "aws_s3_object" "data" {
  for_each = fileset("${path.module}/data","**")

  bucket = aws_s3_bucket.data_bucket.bucket
  key    = each.value
  source = "${path.module}/data/${each.value}"
  source_hash = filemd5("${path.module}/data/${each.value}")
}

# Add Glue Catalog Database
resource "aws_glue_catalog_database" "taxi_db" {
  name = "taxi_db"
}

# Add Glue Crawler
resource "aws_glue_crawler" "taxi_crawler" {
  database_name = aws_glue_catalog_database.taxi_db.name
  name          = "taxi_crawler"
  role          = var.glue_role_arn

  s3_target {
    path = "s3://${aws_s3_bucket.data_bucket.bucket}"
  }
  configuration = <<EOF
  {
    "Version":1.0,
    "Grouping": {
      "TableLevelConfiguration": 2,
      "TableGroupingPolicy": "CombineCompatibleSchemas"
    },
    "CrawlerOutput": {
      "Tables":{
        "TableThreshold":3
      }
    }
  }
  EOF
}

# Add Glue DQ Job Script
resource "aws_s3_object" "script" {
  bucket = var.glue_asset_bucket
  key    = "/scripts/yellow_taxi_dq.py"
  source = "${path.module}/glue/yellow_taxi_dq.py"
  source_hash = filemd5("${path.module}/glue/yellow_taxi_dq.py")
}

# Add Glue DQ Job from Script
resource "aws_glue_job" "taxi_dq_job" {
  name     = "taxi_dq_job"
  role_arn = var.glue_role_arn

  command {
    script_location = "s3://${var.glue_asset_bucket}${aws_s3_object.script.key}"
  }
  timeout = 15
  number_of_workers = 2
  worker_type = "G.1X"
  glue_version = "4.0"
}