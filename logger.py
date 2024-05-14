from flask import Flask, request, jsonify
import logging
import os
import json
from datetime import datetime


app = Flask(__name__)

class LogIngestor:
    def __init__(self, log_directory):
        self.log_directory = log_directory
        self.loggers = {}

    def _get_logger(self, source):
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
        if source not in self.loggers:
            logger = logging.getLogger(source)
            logger.setLevel(logging.INFO)
            file_handler = logging.FileHandler(os.path.join(self.log_directory, f"{source}"))
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            self.loggers[source] = logger
        return self.loggers[source]

    def log(self, level, log_string, source):
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        log_data = {
            "level": level,
            "log_string": log_string,
            "timestamp": timestamp,
            "metadata": {"source": source}
        }
        logger = self._get_logger(source)
        logger.info(json.dumps(log_data))


log_ingestor = LogIngestor(log_directory="logs")

@app.route("/add_log", methods=["POST"])
def add_log():
    data = request.get_json()
    if "level" not in data or "log_string" not in data or "source" not in data:
        return jsonify({"error": "Invalid log data. Required fields: level, log_string, source"}), 400
    log_level = data["level"]
    log_string = data["log_string"]
    source = data["source"]
    log_ingestor.log(level=log_level, log_string=log_string, source=source)
    return jsonify({"message": "Log added successfully."}), 200

if __name__ == "__main__":
    app.run(debug=True)
