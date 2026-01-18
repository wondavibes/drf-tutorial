import requests

try:
    response = requests.get("https://randomuser.me/api/", timeout=5)

    if response.status_code == 200:
        user = response.json()["results"][0]
        print("User:", user["name"]["first"], user["name"]["last"])
    elif response.status_code == 429:
        print("Rate limited by third-party API")
    else:
        print("Unexpected response:", response.text)

except requests.exceptions.Timeout:
    print("Third-party API timed out")
except requests.exceptions.RequestException as e:
    print("API error:", e)
