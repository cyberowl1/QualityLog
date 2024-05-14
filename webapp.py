# backend.py
from flask import Flask, request, jsonify
import os
import glob
import re
import json

app = Flask(__name__)

LOGS_DIR = "logs"

def get_logs():
    logs = []
    for file_path in glob.glob(os.path.join(LOGS_DIR, "*.log")):
        with open(file_path, "r") as file:
            logs.extend(file.readlines())
    return logs


def filter_logs(logs, level=None, log_string=None, source=None):
    filtered_logs = []
    for log in logs:
       
        log_parts = log.split(" - ", maxsplit=2)
        if len(log_parts) != 3:
            print(f"Invalid log format: {log}")
            continue  

    
        timestamp, log_level, metadata_str = log_parts
     
       
        try:
            metadata_dict = json.loads(metadata_str)
            print(metadata_dict.get("source"))
        except json.JSONDecodeError as e:
            print(f"Error parsing metadata: {e}")
            continue

       
        if level and metadata_dict.get("level") != level:
            continue
  
        if log_string and log_string not in metadata_dict.get("log_string"):
            continue
  
        if source and metadata_dict.get("metadata").get("source") != source:
            continue
        
        filtered_logs.append(log.strip())  

    return filtered_logs







@app.route("/query_logs", methods=["GET"])
def query_logs():
    level = request.args.get("level")
    log_string = request.args.get("log_string")
    source = request.args.get("source")
    print(level,log_string,source,"Hey")
    logs = get_logs()
    filtered_logs = filter_logs(logs, level, log_string, source)
    return jsonify({"logs": filtered_logs})

if __name__ == "__main__":
    app.run(debug=True)
