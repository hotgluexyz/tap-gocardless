"""REST client handling, including GoCardlessStream base class."""

import requests
from typing import Any, Dict, Optional

from memoization import cached

from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
import time


class GoCardlessStream(RESTStream):
    """GoCardless stream class."""

    @property
    def url_base(self) -> str:
        if self.config.get("sandbox"):
            return "https://api-sandbox.gocardless.com"
        return "https://api.gocardless.com"

    @property
    def records_jsonpath(self) -> str:
        return f"$.{self.name}[*]"

    next_page_token_jsonpath = "$.meta.cursors.after"
    _page_size = 100
    api_version = "2015-07-06"

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Return a new authenticator object."""
        # GoCardless oAuth2 flow generates a access token which is like a api key and does not expire
        token = self.config.get("access_token") or self.config.get("api_key")
        if not token:
            raise Exception("Access token or api key required")
        return BearerTokenAuthenticator.create_for_stream(self, token=token)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        headers["GoCardless-Version"] = self.api_version
        return headers

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["limit"] = self._page_size
        if next_page_token:
            params["after"] = next_page_token
        return params

    def validate_response(self, response: requests.Response) -> None:
        headers = response.headers
        if "ratelimit-remaining" in headers:
            if int(headers["ratelimit-remaining"]) < self._page_size:
                # The 1000 request per minute
                # TODO utlize ratelimit-reset header value when available
                time.sleep(60)
        if (
            response.status_code in self.extra_retry_statuses
            or 500 <= response.status_code < 600
        ):
            msg = self.response_error_message(response)
            raise RetriableAPIError(msg, response)
        elif 400 <= response.status_code < 500:
            msg = self.response_error_message(response)
            raise FatalAPIError(msg)
