import cripto_cost_service
import unittest
from unittest import mock


class CriptoCostServiceTest(unittest.TestCase):
    test_pair = 'USDT-RUB'
    test_url = f'https://api.coinbase.com/v2/prices/{test_pair}/spot'
    test_response_json = {"data": {"amount": "95.19203206401", "base": "USDT", "currency": "RUB"}}
    test_result = cripto_cost_service.CostResult('95.19203206401', 'RUB')

    def test_send_request(self):
        with mock.patch('cripto_cost_service.requests.get') as mock_get:
            mock_response_success = mock.Mock()
            mock_response_success.status_code = 200
            mock_response_success.json.return_value = self.test_response_json
            mock_get.return_value = mock_response_success

            response = cripto_cost_service.send_request(self.test_url)

            self.assertIsNotNone(response)
            self.assertIsNotNone(response.json())
            self.assertEqual(response.json(), self.test_response_json)

    def test_cost(self):
        with mock.patch('cripto_cost_service.requests.get') as mock_get:
            mock_response_success = mock.Mock()
            mock_response_success.status_code = 200
            mock_response_success.json.return_value = self.test_response_json

            mock_response_error = mock.Mock()
            mock_response_error.status_code = 400
            mock_response_error.json.return_value = None

            mock_get.return_value = mock_response_success

            result_success = cripto_cost_service.cost(self.test_pair)

            self.assertIsNotNone(result_success)
            self.assertEqual(result_success.amount, self.test_result.amount)
            self.assertEqual(result_success.currency, self.test_result.currency)

            mock_get.return_value = mock_response_error
            result_success = cripto_cost_service.cost(self.test_pair)

            self.assertIsNotNone(result_success)
            self.assertEqual(result_success.amount, '-')
            self.assertEqual(result_success.currency, '-')


