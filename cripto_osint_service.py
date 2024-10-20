import logging

import requests

import main

url = 'http://localhost:8190/api/v1/check_address/{address}'


class CheckResult:
    def __init__(self, address: str, found: bool, links_count: int, state: str):
        self.address = address
        self.found = found
        self.links_count = links_count
        self.state = state
    def get_desc(self):
        if self.found :
            return f'Найдена информация об адресе {self.address}\nКоличество упоминаний: {self.links_count}\nСтатус адреса в системе: {self.state}'
        else:
            return f'Адрес {self.address} не найден в системе'

def check_address(address: str):
    send_url = url.format(address=address)
    try:
        logging.debug(f"<GET {send_url}")
        r = send_request(send_url)
        if r.status_code == 200:
            logging.debug(f"<GET {send_url} - SUCCESSES")
            data = r.json()['data']
            return CheckResult(data['address'], data['found'], data['links_count'], data['state'])
    except Exception as e:
        logging.debug(f"<GET failed {send_url}>", e)
        return None
def send_request(send_url:str):
    if main.MOCK_MODE:
        from requests.models import Response
        the_response = Response()
        the_response.code = "success"
        the_response.error_type = "success"
        the_response.status_code = 200
        the_response._content = b'{"data":{"address":"1Cd8nZHAYFH7ZG8aJ1wfhCXhHuxzeRtqoB","found":true,"links_count":12, "state":"Not confirmed"}}'
        return the_response
    else:
        return requests.get(send_url, headers=None, timeout=20)


# def send_scam():
#     send_url = url.format(address=address)
#     try:
#         logging.debug(f"<GET {send_url}")
#         r = requests.get(send_url, headers=None, timeout=20)
#         if r.status_code == 200:
#             logging.debug(f"<GET {send_url} - SUCCESSES")
#             data = r.json()['data']
#             return CheckResult(data['address'], data['found'], data['links_count'], data['state'])
#     except Exception as e:
#         logging.debug(f"<GET failed {send_url}, {e}")
#         return None
# print(url.format(pair ='1111'))
