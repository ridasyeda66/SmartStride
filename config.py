import os

#TODO
#API key for Google Generative AI 
api_key="WRITE_HERE_GEMINI_AI_KEY"
gcs_path_file = "WRITE_HERE_JSON_KEY_FILE_PATH"

def setup_gcp():
    # Set the path to the service account key located in the current folder
    credential_path = os.path.join(os.path.dirname(__file__), gcs_path_file)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# Model configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 300,
    "response_mime_type": "text/plain",
}
