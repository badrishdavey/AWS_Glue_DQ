import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node yellow_taxi
yellow_taxi = glueContext.create_dynamic_frame.from_catalog(
    database="taxi_db",
    table_name="yellow_taxi",
    transformation_ctx="yellow_taxi",
)

# Script generated for node reference
reference = glueContext.create_dynamic_frame.from_catalog(
    database="taxi_db",
    table_name="reference",
    transformation_ctx="reference",
)

# Script generated for node Evaluate Data Quality
EvaluateDataQuality_ruleset = """
    Rules = [
        ColumnCount = 19,
        ReferentialIntegrity "dolocationid" "reference.{locationid}" = 1.0,
        ReferentialIntegrity "pulocationid" "reference.{locationid}" = 1.0
    ]
"""

EvaluateDataQuality_additional_sources = {
    "reference": reference
}

EvaluateDataQuality = EvaluateDataQuality().process_rows(
    frame=yellow_taxi,
    additional_data_sources=EvaluateDataQuality_additional_sources,
    ruleset=EvaluateDataQuality_ruleset,
    publishing_options={
        "dataQualityEvaluationContext": "EvaluateDataQuality",
        "enableDataQualityCloudWatchMetrics": True,
        "enableDataQualityResultsPublishing": True,
    },
    additional_options={
        "observations.scope": "ALL",
        "performanceTuning.caching": "CACHE_NOTHING",
    },
)

# Script generated for node ruleOutcomes
ruleOutcomes = SelectFromCollection.apply(
    dfc=EvaluateDataQuality,
    key="ruleOutcomes",
    transformation_ctx="ruleOutcomes",
)

job.commit()

assert (
    ruleOutcomes.toDF().filter("Outcome == 'Failed'")
    .count()
    == 0
), "The job failed due to failing DQ rules"
