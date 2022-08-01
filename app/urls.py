from dataclasses import dataclass

CLOUD_PAYMENTS = 'https://api.cloudpayments.ru'


@dataclass
class CloudPaymentsUrls:
    charge_pay = '/payments/charge/'