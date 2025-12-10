from google.cloud import aiplatform
from pipeline import calculation_pipeline
from kfp import compiler

# --- User configuration ---
PROJECT_ID = "YOUR_PROJECT_ID"
REGION = "YOUR_REGION"
PIPELINE_ROOT = "gs://YOUR_GCS_BUCKET/pipeline-root"
# --------------------------

PIPELINE_JSON = "calculation_pipeline.json"

def run_pipeline():
    """Compiles and runs the pipeline."""

    # Compile the pipeline
    compiler.Compiler().compile(
        pipeline_func=calculation_pipeline,
        package_path=PIPELINE_JSON
    )

    # Initialize the AI Platform client
    aiplatform.init(project=PROJECT_ID, location=REGION)

    # Create a pipeline job
    job = aiplatform.PipelineJob(
        display_name="calculation-pipeline-run",
        template_path=PIPELINE_JSON,
        pipeline_root=PIPELINE_ROOT,
        parameter_values={
            'num1': 15,
            'num2': 7
        }
    )

    # Submit the pipeline job
    job.submit()
    print(f"Pipeline job submitted. View it here: {job.dashboard_uri}")

if __name__ == '__main__':
    run_pipeline()
