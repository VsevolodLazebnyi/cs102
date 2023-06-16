import typing as tp

import requests  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from requests.packages.urllib3.util.retry import Retry  # type: ignore


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.session = requests.Session()
        self.session.mount(
            prefix="https://",
            adapter=HTTPAdapter(
                max_retries=Retry(
                    backoff_factor=backoff_factor,
                    total=max_retries,
                    status_forcelist=[500, 502, 503, 504],
                )
            ),
        )
        self.timeout = timeout
        self.base_url = base_url

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        response = self.session.get(url=f"{self.base_url}/{url}", params=kwargs, timeout=self.timeout)
        return response

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        response = self.session.post(url=f"{self.base_url}/{url}", data=kwargs, timeout=self.timeout)
        return response
