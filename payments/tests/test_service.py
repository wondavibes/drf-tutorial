from unittest.mock import patch
from payments.services import verify_transaction


@patch("payments.services.requests.get")
def test_verify_transaction_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": {"status": "success"}}

    result = verify_transaction("ref_test_123")

    assert result is True
