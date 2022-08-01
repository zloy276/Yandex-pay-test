# yandex-pay-test

Реализация Python клиента для Cloudpayments API. Для авторизации используются Public ID(логин) и API Secret(логин), которые предварительно нужно взять из сервиса Yandex Pay. В сервисе используется идемпотентный API, для предотвращения получения идентичных ответов передавать request_id  
`CloudPaymentsClient(public_id, api_secret, request_id).pay(**params)`

Поля для параметров запроса можно найти в [документации](https://developers.cloudpayments.ru/#oplata-po-kriptogramme)
Поля необходимо указывать в PascalCase
  
- Реализована Basic [авторизация](./app/auth.py)
