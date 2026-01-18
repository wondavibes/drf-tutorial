import requests

BASE_URL = "http://127.0.0.1:8000"


def login():
    response = requests.post(
        f"{BASE_URL}/api/token/",
        json={
            "username": "admin",
            "password": "noteadmin14",
        },
    )
    response.raise_for_status()
    return response.json()


tokens = login()
access = tokens["access"]
refresh = tokens["refresh"]


def refresh_access_token(refresh_token):
    response = requests.post(
        f"{BASE_URL}/api/token/refresh/",
        json={"refresh": refresh_token},
    )
    response.raise_for_status()
    return response.json()["access"]


def get_notes(access_token, refresh_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/api/notes/", headers=headers)

    if response.status_code == 401:
        # Access token might be expired, try refreshing
        new_access_token = refresh_access_token(refresh_token)
        headers = {"Authorization": f"Bearer {new_access_token}"}
        response = requests.get(f"{BASE_URL}/api/notes/", headers=headers)
        response.raise_for_status()
        return response.json(), new_access_token

    response.raise_for_status()
    return response.json(), access_token


notes, access = get_notes(access, refresh)
print(notes)
print(access)
