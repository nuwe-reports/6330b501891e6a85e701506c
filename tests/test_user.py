import requests
import json

testing_server = "http://127.0.0.1:8000"


def test_job_posts_register():
    data = dict(
        {
            "username": "Fake User",
            "email": "fakeuser@fakecompany.com",
            "password": "12345678",
        }
    )
    response = requests.post(
        f"{testing_server}/API/v1/users/register",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201

    # Already registered user
    response = requests.post(
        f"{testing_server}/API/v1/users/register",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400


def test_job_posts_subscriptions():
    response = requests.get(f"{testing_server}/API/v1/users/list")
    assert response.json()["body"][-1]["subscribed"]

    # Test unsubcriptions
    email = response.json()["body"][-1]["email"]
    response = requests.get(
        f"{testing_server}/API/v1/users/unsubscribe/{email}",
    )
    response = requests.get(f"{testing_server}/API/v1/users/list")
    assert not response.json()["body"][-1]["subscribed"]

    # Test subcriptions
    response = requests.get(
        f"{testing_server}/API/v1/users/subscribe/{email}",
    )
    response = requests.get(f"{testing_server}/API/v1/users/list")
    assert response.json()["body"][-1]["subscribed"]

    # Delete user
    response = requests.delete(f"{testing_server}/API/v1/users/delete/{email}")
    assert response.status_code == 200
