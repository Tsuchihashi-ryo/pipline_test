# config.py
# Central configuration for the pipeline.

# All components in this pipeline will use this Docker image.
# Replace this with the URI of the image you built and pushed to Artifact Registry.
BASE_IMAGE = 'gcr.io/YOUR_PROJECT_ID/pipeline-components:latest'
