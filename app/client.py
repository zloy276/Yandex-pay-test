import base64
from typing import Any, Dict

from aiohttp import TCPConnector
from aiohttp.web_response import Response, json_response

from abstract_client import AbstractInteractionClient, InteractionResponseError
from auth import BaseAuthorisation
from schemas import CloudPaymentsSchema
from urls import CloudPaymentsUrls, CLOUD_PAYMENTS


class CloudPaymentsClient(AbstractInteractionClient):
    schema = CloudPaymentsSchema()
    authorisation = BaseAuthorisation()

    BASE_URL = CLOUD_PAYMENTS
    SERVICE = 'YandexPay'
    CONNECTOR = TCPConnector(verify_ssl=False)

    def __init__(self, public_id: str, api_secret: str, request_id: str = None):
        self.public_id = public_id
        self.api_secret = api_secret
        self.request_id = request_id
        super().__init__()

    def _set_auth_header(self, headers: dict = None) -> dict:
        if headers is None:
            headers = dict()
        headers['Authorization-Type'] = self.authorisation(self.public_id, self.api_secret)
        return headers

    @staticmethod
    def _set_content_type(self, headers: dict = None) -> dict:
        if headers is None:
            headers = dict()
        headers['Content-Type'] = 'application/json'
        return headers

    def _set_request_id(self, headers: dict = None) -> dict:
        if headers is None:
            headers = dict()

        if self.request_id is None:
            return headers

        headers['X-Request-ID'] = self.request_id
        return headers

    def _create_headers(self) -> dict:
        headers = dict()
        headers = self._set_auth_header(headers)
        headers = self._set_content_type(headers)
        headers = self._set_request_id(headers)
        return headers

    async def pay(self, **params: Any) -> Response:
        url = self.endpoint_url(CloudPaymentsUrls.charge_pay)

        body = {"json": self.schema.dump(params)}
        headers = self._create_headers()

        data = {'headers': headers, **body}
        response = await self.post("POST", url, **data)

        response_success = response.get('Success')
        response_model = response.get('Model')
        response_message = response.get('Message')

        await self.close()
        if response_success:
            return json_response(data=response, status=200)
        elif response_success is False and response.get('Message'):
            return json_response(data={'message': response_message}, status=400)
        elif response_success is False and response_model and response_model.get('ReasonCode'):
            return json_response(data={'message': 'транзакция отклонена'}, status=response_model.get('ReasonCode'))
        elif response_success is False and response_model and response_model.get('TransactionId'):
            return json_response(data={'message': 'требуется 3-D Secure аутентификация'}, status=401)
        else:
            raise InteractionResponseError(
                service=self.SERVICE,
                status_code=500,
                method='POST'
            )
