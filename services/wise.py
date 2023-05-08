import json
import uuid
import requests
from decouple import config
from fastapi import HTTPException


class WiseService:
    def __init__(self) -> None:
        self.main_url = config("WISE_URL")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}"
        }
        self.profile_id = self._get_profile__id()

    def _get_profile__id(self):
        url = self.main_url + "v2/profiles"
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                return [el["id"] for el in response.json() if el["type"] == "PERSONAL"][0]
        except Exception:
            raise HTTPException(500, "The payment gateway has issue ,please try later")

    def create_a_quote(self, amount):
        url = self.main_url + "v3/profiles/" + str(self.profile_id) + "/quotes"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "targetAmount": amount,
            "profile": self.profile_id,
        }
        try:
            response = requests.post(url=url, data=json.dumps(data), headers=self.headers)
            if response.status_code == 200:
                return response.json()["id"]
            else:
                raise HTTPException(500, "Payment Gateway has issue to create Quotes")
        except Exception:
            raise HTTPException(500, "Payment Gateway has issue to create Quotes")

    def create_recipient(self, full_name, iban):
        url = self.main_url + "v1/accounts"
        data = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "accountHolderName": full_name,
            "legalType": "PRIVATE",
            "details": {"iban": iban},
        }
        try:
            print(json.dumps(data))
            response = requests.post(url=url, data=json.dumps(data), headers=self.headers)
            if response.status_code == 200:
                return response.json()["id"]
            else:
                raise HTTPException(500, "Payment Gateway has issue to create Quotes")
        except Exception:
            raise HTTPException(500, "Payment Gateway has issue to create Quotes")

    def create_transfer(self, target_account_id, quote_id):
        url = self.main_url + "/v1/transfers"
        data = {"targetAccount": target_account_id,
                "quoteUuid": quote_id, "customerTransactionId": str(uuid.uuid4()),
                "details": {"reference": "Testing",
                            "transferPurpose": "Refund for the purchased goods",
                            "transferPurposeSubTransferPurpose": "Repay ment for the faulty item",
                            "sourceOfFunds": "from purchase payment"
                            }
                }
        try:
            response = requests.post(url=url, data=json.dumps(data), headers=self.headers)
            print(json.dumps(response.json(), indent=2))
            if response.status_code == 200:

                return response.json()["id"]
            else:
                raise HTTPException(500, "Payment Gateway has issue to create Quotes")
        except Exception:
            raise HTTPException(500, "Payment Gateway has issue to create Quotes")

    def fund_transfer(self, transfer_id):
        url = self.main_url + "v3/profiles/" + str(self.profile_id) + "/transfers/" + str(transfer_id) + "/payments"
        data = {"type": "BALANCE"
                }
        try:
            response = requests.post(url=url, data=json.dumps(data), headers=self.headers)
            print(json.dumps(response.json(), indent=2))
            print(response.status_code)
            if response.status_code == 201:

                return response.json()["balanceTransactionId"]
            else:
                raise HTTPException(500, "Payment Gateway has issue in Fund Transfer")
        except Exception:
            raise HTTPException(500, "Payment Gateway has issue in Fund Transfer")

    def fund_transfer_cancel(self, transfer_id):
        url = self.main_url + "v1/transfers/" + str(transfer_id) + "/cancel"
        try:
            response = requests.put(url=url, headers=self.headers)
            if response.status_code == 200:

                return response.json()["id"]
            else:
                raise HTTPException(500, "Payment Gateway has issue in Cancel Transfer")
        except Exception:
            raise HTTPException(500, "Payment Gateway has issue in Cancel Transfer")
