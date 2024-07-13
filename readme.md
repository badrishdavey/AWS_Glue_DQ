### 1. Update terraform.tfvars file 
    region          = "us-east-1"
    tf_state_bucket = "<my-bucket-for-tfstate>"
    glue_asset_bucket = "aws-glue-assets-<accountNumber>-us-east-1"
    data_bucket   = "<my-bucket-for-taxi-data>"
    glue_role_arn = "arn:aws:iam::<accountNumber>:role/GlueRole"

### 2. Add GitHub Environment Variable for "TF_API_TOKEN"
Follow [these](https://developer.hashicorp.com/terraform/tutorials/automation/github-actions) instructions to set things correctly.

### 3. Update GitHub Actions 'TF_CLOUD_ORGANIZATION' to your repo name
Ex. jaredfiacco2 if your username is jaredfiacco2

### 4. Run Glue Crawler
<img src="images\run_glue_crawler.jpg"/>

### 5. Run Glue Job
<img src="images\run_glue_crawler.jpg"/>

### 6. Check Data Quality1
<img src="images\review_dq_results.jpg"/>
