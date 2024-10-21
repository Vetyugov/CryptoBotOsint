import logging

import requests

import main

url = 'https://api.coinbase.com/v2/prices/{pair}/spot'

class CostResult:
    def __init__(self, amount: str, currency: str):
        self.amount = amount
        self.currency = currency


def cost(cripto_pair: str):
    send_url = url.format(pair=cripto_pair)
    try:
        logging.debug(f"<GET {send_url}")
        r = send_request(send_url)
        if r.status_code == 200:
            logging.debug(f"<GET {send_url}> - SUCCESSES response: {r.json()}")
            data = r.json()['data']
            result = CostResult(data['amount'], data['currency'])
            return result
    except Exception as e:
        print('Произошла ошибка',e )
        logging.error(f"<GET failed {send_url}, {e}")
    return CostResult('-', "-")


def send_request(send_url:str):
    if main.MOCK_MODE:
        from requests.models import Response
        the_response = Response()
        the_response.code = "success"
        the_response.error_type = "success"
        the_response.status_code = 200
        the_response._content = b'{"data":{"amount":"95.19203206401","base":"USDT","currency":"RUB"}}'
        return the_response
    else:
        return requests.get(send_url, headers=None, timeout=20)

# print(url.format(pair ='1111'))
