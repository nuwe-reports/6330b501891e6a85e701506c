import requests
import json

server = "http://127.0.0.1:8000"
data = [
    dict(
        {
            "name": "Data Engineer ACME",
            "company_name": "ACME",
            "job_description": "data engineer",
            "skills": "python, AWS",
            "job_type": "senior",
            "locations": "remote",
            "comments": "best job in the world",
        }
    ),
    dict(
        {
            "name": "Data Scientist RR",
            "company_name": "Red Ribbon",
            "job_description": "data scientist",
            "skills": "python, pytorch",
            "job_type": "junior",
            "locations": "Japan",
            "comments": "best job in the world",
        }
    ),
    dict(
        {
            "name": "Data Scientist Rumasa",
            "company_name": "Rumasa",
            "job_description": "data scientist",
            "skills": "python, R, pytorch, XGBoost",
            "job_type": "senior",
            "locations": "Madrid",
            "comments": "best job in the world",
        }
    ),
]

for job in data:
    response = requests.post(
        f"{server}/API/v1/jobposts/create",
        data=json.dumps(job),
        headers={"Content-Type": "application/json"},
    )
