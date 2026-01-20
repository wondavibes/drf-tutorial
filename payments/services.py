import os
import requests

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
BASE_URL = "https://api.paystack.co"


class PaystackError(Exception):
    # raised when there is an error with Paystack API
    pass


def verify_transaction(reference: str) -> bool:
    if not PAYSTACK_SECRET_KEY:
        raise PaystackError("Paystack secret key not configured")

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(
        f"{BASE_URL}/transaction/verify/{reference}",
        headers=headers,
        timeout=10,
    )
    if response.status_code != 200:
        raise PaystackError("Paystack API Error")

    data = response.json()

    return data["data"]["status"] == "success"
