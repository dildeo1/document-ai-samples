import os
from typing import Dict
import logging

from api.helper import populate_list_source
from api.helper import process_document
from api.helper import store_file
from flask import Flask, jsonify, request
from flask_cors import CORS  # comment this on deployment
from flask_restful import Api
import google.auth

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_, project_id = google.auth.default()
LOCATION = "us"  # Format is 'us' or 'eu'

processor_id_by_processor_type: Dict[str, str] = {}

app = Flask(__name__, static_url_path="", static_folder="")
CORS(app)
api = Api(app)

@app.route("/", methods=["GET"])
def home():
    """Gets all available processors that are in the specified GCP project"""
    logger.info("Home endpoint called")
    populate_list_source(project_id, LOCATION, processor_id_by_processor_type)
    logger.info("Processor list populated")
    print("Processor list populated")
    return jsonify(
        {
            "resultStatus": "SUCCESS",
        }
    )

@app.route("/api/init", methods=["GET"])
def populate_list():
    """Gets all available processors that are in the specified GCP project"""
    logger.info("Populate list endpoint called")
    populate_list_source(project_id, LOCATION, processor_id_by_processor_type)
    logger.info("Processor list populated")
    return jsonify(
        {
            "resultStatus": "SUCCESS",
        }
    )

@app.route("/api/docai", methods=["POST"])
def get_document():
    """Calls process_document and returns document proto"""
    logger.info("DocAI endpoint called")
    directory = "api/test_docs"
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))
    logger.info("Cleared test_docs directory")

    processor_type = request.form["fileProcessorType"]
    logger.info(f"Received processor type: {processor_type}")

    populate_list_source(project_id, LOCATION, processor_id_by_processor_type)
    processor_id = processor_id_by_processor_type.get(processor_type)
    logger.info(f"Processor ID: {processor_id}")

    file = request.files["file"]
    file_type = file.content_type
    logger.info(f"Received file of type: {file_type}")

    try:
        _destination = store_file(file)
        logger.info(f"Stored file at: {_destination}")
    except Exception as err:  # pylint: disable=W0703
        logger.error(f"Error storing file: {err}")
        return {
            "resultStatus": "ERROR",
            "errorMessage": str(err),
        }, 400

    process_document_request = {
        "project_id": project_id,
        "location": LOCATION,
        "file_path": _destination,
        "file_type": file_type,
        "processor_id": processor_id,
    }

    response = process_document(process_document_request)
    logger.info("Processed document")
    return response

@app.route("/api/processor/list", methods=["GET"])
def get_list():
    """Returns list of available processors"""
    logger.info("Processor list endpoint called")
    processor_list = list(processor_id_by_processor_type.keys())
    response = jsonify({"resultStatus": "SUCCESS", "processor_list": processor_list})
    logger.info(f"Processor list: {processor_list}")
    return response

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
