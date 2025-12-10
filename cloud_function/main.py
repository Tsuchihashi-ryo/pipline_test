import os
import functions_framework
from google.cloud import aiplatform
from flask import jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

@functions_framework.http
def trigger_pipeline(request):
    """
    HTTP Cloud Function to trigger a Vertex AI Pipeline.
    The function is triggered by a POST request with a JSON body.
    Example JSON body: {"num1": 10, "num2": 5}
    """
    # --- Configuration ---
    # These should be set as environment variables in the Cloud Function deployment.
    PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    REGION = os.environ.get("GCP_REGION")
    PIPELINE_ROOT = os.environ.get("PIPELINE_ROOT_GCS_PATH")
    PIPELINE_JSON = "calculation_pipeline.json"

    # --- Validate Environment Configuration ---
    if not all([PROJECT_ID, REGION, PIPELINE_ROOT]):
        error_msg = "Missing required environment variables (GCP_PROJECT_ID, GCP_REGION, PIPELINE_ROOT_GCS_PATH)."
        logging.error(error_msg)
        return jsonify({"error": error_msg}), 500

    # --- Parse and Validate Request Body ---
    if not request.is_json:
        return jsonify({"error": "Invalid request: Content-Type must be application/json."}), 400

    request_json = request.get_json()
    if 'num1' not in request_json or 'num2' not in request_json:
        return jsonify({"error": "Invalid request body. Please provide 'num1' and 'num2' keys."}), 400

    try:
        num1 = float(request_json['num1'])
        num2 = float(request_json['num2'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input. 'num1' and 'num2' must be numbers."}), 400

    # --- Initialize Vertex AI Client ---
    logging.info(f"Initializing Vertex AI client for project '{PROJECT_ID}' in region '{REGION}'.")
    aiplatform.init(project=PROJECT_ID, location=REGION)

    # --- Create and Submit Pipeline Job ---
    job = aiplatform.PipelineJob(
        display_name="calculation-pipeline-api-triggered-run",
        template_path=PIPELINE_JSON,
        pipeline_root=PIPELINE_ROOT,
        parameter_values={
            'num1': num1,
            'num2': num2
        }
    )

    try:
        logging.info("Submitting pipeline job.")
        job.submit()
        logging.info(f"Pipeline job submitted. Name: {job.resource_name}")

        response_data = {
            "message": "Pipeline job submitted successfully.",
            "job_name": job.resource_name,
            "dashboard_uri": job.dashboard_uri
        }
        return jsonify(response_data), 202  # 202 Accepted: The request has been accepted for processing

    except Exception as e:
        logging.error(f"Error submitting pipeline job: {e}")
        return jsonify({"error": f"Failed to submit pipeline job: {str(e)}"}), 500
