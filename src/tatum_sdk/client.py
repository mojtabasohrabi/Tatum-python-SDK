"""Tatum SDK client implementation."""
import requests
import random
import json


class TatumAPIError(Exception):
    pass


def _handle_response(response):
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise TatumAPIError(f"Tatum API error: {str(e)}")
    except ValueError:
        raise TatumAPIError("Invalid JSON response from Tatum API")


class TatumClient:
    def __init__(self, api_key: str, blockchain: str = "tron", base_url: str = "https://api.tatum.io"):
        self.api_key = api_key
        self.base_url = base_url
        self.blockchain = blockchain
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        })

    def generate_wallet(self):
        index = random.randint(1, 2147483647)
        mnemonic, xpub = self._generate_mnemonic_and_xpub()
        address = self._generate_address(xpub, index)
        private_key = self._generate_private_key(index, mnemonic)
        response = {
            'index': index,
            'mnemonic': mnemonic,
            'xpub': xpub,
            'address': address["address"],
            'private_key': private_key["key"],
        }
        return response

    def get_account_details(self, address: str) -> dict:
        endpoint = f"{self.base_url}/v3/{self.blockchain}/account/{address}"
        response = self.session.get(endpoint)
        return _handle_response(response)

    def get_all_transactions(self, address: str, only_confirmed: str = None, only_unconfirmed: str = None,
                             only_to: str = None, only_from: str = None, order_by: str = "block_timestamp,asc") -> dict:
        if only_confirmed is not None and only_confirmed not in ("true", "false"):
            raise ValueError("only_confirmed must be either 'true' or 'false'")

        if only_unconfirmed is not None and only_unconfirmed not in ["true", "false"]:
            raise ValueError("only_unconfirmed must be either 'true' or 'false'")

        if only_confirmed is not None and only_unconfirmed is not None and only_confirmed != "true" and only_unconfirmed != "false":
            raise ValueError("Only one of only_confirmed or only_unconfirmed can be set to a non-default value")

        if order_by not in ("block_timestamp,asc", "block_timestamp,desc"):
            raise ValueError("order_by must be either 'block_timestamp,asc' or 'block_timestamp,desc'")

        if only_to is not None and only_from is not None:
            raise ValueError("Only one of only_to or only_from can be provided, not both")

        if only_confirmed is not None and only_unconfirmed is not None:
            raise ValueError("Only one of only_confirmed or only_unconfirmed can be provided, not both")

        endpoint = f"{self.base_url}/v3/{self.blockchain}/transaction/account/{address}?"

        if only_confirmed is not None and only_confirmed != "true":
            endpoint += f"onlyConfirmed={only_confirmed}&"
        elif only_unconfirmed is not None and only_unconfirmed != "false":
            endpoint += f"onlyUnconfirmed={only_unconfirmed}&"

        if only_to is not None:
            endpoint += f"onlyTo={only_to}&"
        elif only_from is not None:
            endpoint += f"onlyFrom={only_from}&"

        endpoint += f"orderBy={order_by}"

        endpoint = endpoint.rstrip("&").rstrip("?")

        response = self.session.get(endpoint)
        return _handle_response(response)

    def _generate_private_key(self, index, mnemonic):
        endpoint = f"{self.base_url}/v3/{self.blockchain}/wallet/priv"
        data = json.dumps({
            "mnemonic": mnemonic,
            "index": index
        })
        response = self.session.post(endpoint, data=data)
        return _handle_response(response)

    def _generate_address(self, xpub, index):
        endpoint = f"{self.base_url}/v3/{self.blockchain}/address/{xpub}/{index}"
        response = self.session.get(endpoint)
        return _handle_response(response)

    def _generate_mnemonic_and_xpub(self):
        endpoint = f"{self.base_url}/v3/{self.blockchain}/wallet"
        response = self.session.get(endpoint)
        response = response.json()
        return response["mnemonic"], response["xpub"]
