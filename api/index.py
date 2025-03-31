import csv
import json
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])

github_csv_url = "https://raw.githubusercontent.com/MiryalaNarayanaReddy/tds-project-scheduled-workflow/refs/heads/master/q-fastapi.csv"

def fetch_csv_data() -> Dict[str, List[Dict[str, str]]]:
    response = requests.get(github_csv_url)
    response.raise_for_status()
    
    decoded_content = response.content.decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_content)
    
    students = [
        {"studentId": int(row["studentId"]), "class": row["class"]}
        for row in reader
    ]
    return {"students": students}

@app.get("/api")
def get_students(class_param: List[str] = Query(None, alias="class")):
    json_output = fetch_csv_data()
    if class_param is None:
        return json_output  # Return all students if no class filter is applied
    filtered_students = [s for s in json_output["students"] if s["class"] in class_param]
    return {"students": filtered_students}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
