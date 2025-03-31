import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])

github_json_url = "https://raw.githubusercontent.com/MiryalaNarayanaReddy/tds-project-scheduled-workflow/refs/heads/master/q-vercel-python.json"

def fetch_json_data() -> Dict[str, int]:
    """Fetch JSON data and return a dictionary mapping names to marks."""
    response = requests.get(github_json_url)
    response.raise_for_status()
    data = response.json()

    # Convert list of dictionaries into a name-to-marks mapping
    marks_dict = {entry["name"]: entry["marks"] for entry in data}
    return marks_dict

@app.get("/api")
def get_marks(name: List[str] = Query(...)):
    """Return marks in the same order as requested names."""
    marks_dict = fetch_json_data()

    # Extract marks for the requested names (return 0 if name not found)
    marks = [marks_dict.get(n, 0) for n in name]
    return {"marks": marks}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
