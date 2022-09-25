import requests
import json

testing_server = "http://127.0.0.1:8000"


def test_job_posts_create():
    data = dict(
        {
            "name": "Fake job post",
            "company_name": "Fake company",
            "job_description": "Fake data engineer",
            "skills": "python, AWS",
            "job_type": "senior",
            "locations": "remote",
            "comments": "best fake job in the world",
        }
    )
    response = requests.post(
        f"{testing_server}/API/v1/jobposts/create",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201


def test_job_posts_list():
    response = requests.get(f"{testing_server}/API/v1/jobposts/list")
    assert len(response.json()["body"]) > 0
    assert response.status_code == 200


def test_job_posts_put():
    new_location = "Ulldecona"
    response = requests.get(f"{testing_server}/API/v1/jobposts/search?name=fake")
    id = response.json()["body"][-1]["id"]

    data = dict({"locations": new_location})
    response = requests.put(
        f"{testing_server}/API/v1/jobposts/update/{id}",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201

    response = requests.get(f"{testing_server}/API/v1/jobposts/search?name=fake")
    location = response.json()["body"][-1]["locations"]

    assert location == new_location


def test_job_posts_search_and_delete():
    response = requests.get(f"{testing_server}/API/v1/jobposts/search?name=fake")
    id = response.json()["body"][-1]["id"]
    response = requests.delete(f"{testing_server}/API/v1/jobposts/delete/{id}")
    assert response.status_code == 200
