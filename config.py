import os

def setup_gcp():
    # Set the path to the service account key located in the current folder
    credential_path = os.path.join(os.path.dirname(__file__), "aiatl-439722-78a2f30a5602.json")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


#API key for Google Generative AI 
api_key="AIzaSyBzSTcxvJN_-8pe-EMrvdjiUxf0Z2sYkvE"

# Model configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 300,
    "response_mime_type": "text/plain",
}