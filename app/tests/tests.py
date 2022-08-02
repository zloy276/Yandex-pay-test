import base64
from unittest import IsolatedAsyncioTestCase, mock
from uuid import uuid4

from abstract_client import InteractionResponseError
from client import CloudPaymentsClient
from parameterized import parameterized

from fixtures import PREPARED_PARAMS, RESPONSES


class ResponseMockedTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.public_id, self.api_secret = str(uuid4()), str(uuid4())
        self.payment_token = base64.b64encode(bytes(str(uuid4()), 'utf-8'))

    @parameterized.expand(RESPONSES)
    async def test_responses(self, mock_response, status):
        mock_request = mock.patch(
            "abstract_client.AbstractInteractionClient._request",
            mock.AsyncMock(return_value=mock_response)
        )
        with mock_request as _:
            client = CloudPaymentsClient(self.public_id, self.api_secret)
            response = await client.pay(**PREPARED_PARAMS)
        self.assertEqual(status, response.status)
