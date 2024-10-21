import unittest
from unittest import mock

import cripto_osint_service


class CriptoOsintServiceTest(unittest.TestCase):
    test_address = 'asdfFGqwr12345t'
    test_url = f'http://localhost:8190/api/v1/check_address/{test_address}'
    test_response_json = {"data": {"address": test_address, "found": True, "links_count": 12,
                                   "state": "Not confirmed"}}
    test_result = cripto_osint_service.CheckResult(test_address, True, 12, 'Not confirmed')

    def test_send_request(self):
        with mock.patch('cripto_osint_service.requests.get') as mock_get:
            mock_response_success = mock.Mock()
            mock_response_success.status_code = 200
            mock_response_success.json.return_value = self.test_response_json
            mock_get.return_value = mock_response_success

            response = cripto_osint_service.send_request(self.test_url)

            self.assertIsNotNone(response)
            self.assertIsNotNone(response.json())
            self.assertEqual(response.json(), self.test_response_json)

    def test_check_address(self):
        with mock.patch('cripto_osint_service.requests.get') as mock_get:
            mock_response_success = mock.Mock()
            mock_response_success.status_code = 200
            mock_response_success.json.return_value = self.test_response_json

            mock_response_error = mock.Mock()
            mock_response_error.status_code = 400
            mock_response_error.json.return_value = None

            mock_get.return_value = mock_response_success

            result_success = cripto_osint_service.check_address(self.test_address)

            self.assertIsNotNone(result_success)
            self.assertEqual(result_success.address, self.test_result.address)
            self.assertEqual(result_success.found, self.test_result.found)
            self.assertEqual(result_success.links_count, self.test_result.links_count)
            self.assertEqual(result_success.state, self.test_result.state)

            mock_get.return_value = mock_response_error
            result_success = cripto_osint_service.check_address(self.test_address)

            self.assertIsNone(result_success)

    def test_get_desc(self):
        found_check_result = cripto_osint_service.CheckResult('12345', True, 12, 'Not confirmed')

        not_found_check_result = cripto_osint_service.CheckResult('12345', False, 0, '-')

        self.assertEqual(found_check_result.get_desc(),
                         'Найдена информация об адресе 12345\nКоличество упоминаний: 12\nСтатус адреса в системе: Not confirmed')
        self.assertEqual(not_found_check_result.get_desc(),
                         'Адрес 12345 не найден в системе')
