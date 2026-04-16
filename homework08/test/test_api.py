import requests

url = "http://127.0.0.1:5000"

response_help = requests.get(f"{url}/help")
response_data = requests.get(f"{url}/data")
response_countries = requests.get(f"{url}/countries")


def test_help():
    assert response_help.status_code == 200
    assert isinstance(response_help.json(), dict) == True


def test_data():
    assert response_data.status_code == 200
    assert isinstance(response_data.json(), list) == True


def test_countries():
    assert response_countries.status_code == 200
    assert isinstance(response_countries.json(), list) == True


def test_specific_country():
    if len(response_countries.json()) > 0:
        key = response_countries.json()[0]
        country_code, year = key.split(":")
        response = requests.get(f"{url}/countries/{country_code}/{year}")

        assert response.status_code == 200
        assert isinstance(response.json(), dict) == True


def test_jobs_post():
    payload = {
        "country_code": "USA",
        "start_year": 2000,
        "end_year": 2005
    }

    response = requests.post(f"{url}/jobs", json=payload)

    assert response.status_code in [200, 400]
    assert isinstance(response.json(), dict)


def test_jobs_get():
    response = requests.get(f"{url}/jobs")

    assert response.status_code == 200
    assert isinstance(response.json(), list) == True


def test_results():
    response = requests.get(f"{url}/results/fake_id")

    assert response.status_code == 404
    assert isinstance(response.json(), dict) == True
