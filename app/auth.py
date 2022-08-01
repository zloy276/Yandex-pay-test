from base64 import b64encode


class BaseAuthorisation:
    def __call__(self, username: str, password: str) -> str:
        if isinstance(username, str):
            username = username.encode()

        if isinstance(password, str):
            password = password.encode()

        auth = b64encode(b":".join((username, password))).strip()

        return f'Basic {auth}'
