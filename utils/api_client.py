"""
A small HTTP client for tests that need to talk to a backend, not just tap
through the app — fetching an OTP, seeding data, checking what the API really
stored after a booking.

Three ways in:

    # 1. the Swing backend, with the headers the app sends
    api = ApiClient.swing()
    code = otp_code(api.request_otp("82165162549", "+62", "WHATSAPP"))

    # 2. any other API, straight from .env, one prefix per API
    #    BOOKING_API_URL, BOOKING_API_HEADERS, BOOKING_API_RETRIES, ...
    api = ApiClient.from_env("BOOKING_API")

    # 3. spelled out in code
    api = ApiClient("https://api.getswing.dev", headers={"x-api-key": key})
    booking = api.get("/v1/bookings/{id}", id=booking_id).pick("data.status")

Placeholders — `{name}` anywhere in the url, params, headers or body is filled
from the keyword arguments you pass to the call (and url-encoded in the URL):

    api.get("/qa/otp?phone={phone}", phone="+62812...")

For from_env(), every key below is optional except the URL. Swap the prefix
and the same knobs work for any API:

    <PREFIX>_URL          https://api.getswing.dev/v1/bookings/{id}
    <PREFIX>_METHOD       GET (default) / POST / PUT / PATCH / DELETE
    <PREFIX>_HEADERS      {"x-api-key": "..."}      JSON object
    <PREFIX>_PARAMS       {"country": "62"}         JSON object -> query string
    <PREFIX>_BODY         {"phone": "{phone}"}      JSON object -> request body
    <PREFIX>_TIMEOUT      seconds per request (10)
    <PREFIX>_RETRIES      attempts before giving up (1)
    <PREFIX>_RETRY_DELAY  seconds between attempts (3)
"""
import json
import os
import re
import time
from urllib.parse import quote


class ApiError(RuntimeError):
    """A request failed, or never returned what the caller was waiting for."""


# ---------------------------------------------------------------------------
# the Swing backend
# ---------------------------------------------------------------------------
# Defaults are the dev environment. Every one is overridable from .env, so the
# same calls run against another environment (or another device fingerprint)
# without touching this file.
SWING_BASE_URL = "https://api-dev.getswing.cloud"
SWING_OTP_REQUEST_PATH = "/players/api/v1/auth/otp/request"

# Keys we look at when SWING_OTP_FIELD is not set — whichever one the OTP
# endpoint answers with.
OTP_KEYS = ("otp", "code", "otp_code", "otpCode", "verification_code",
            "verificationCode", "pin")


def swing_headers() -> dict:
    """The header set the mobile app sends. content-length is left out on
    purpose — requests sets it from the body."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": os.getenv("SWING_API_KEY", "ZGV2LXB1YmxpYy1hcGkta2V5"),
        "X-Device": os.getenv("SWING_DEVICE", "android-5.1.0-DEV.20260812+1786530371"),
        "X-Timezone": os.getenv("SWING_TIMEZONE", "WIB"),
        "X-Package-Name": os.getenv("APP_PACKAGE", "app.getswing.dev"),
        "X-SOURCE": os.getenv("SWING_SOURCE", "MOBILE_PLAYERS"),
        "X-Device-Id": os.getenv(
            "SWING_DEVICE_ID", "android_Google_sdk_gphone64_arm64_622e541f1ab5c539"
        ),
        "X-Geo-Country": os.getenv("SWING_GEO_COUNTRY", "ID"),
        "X-Filter-Country": os.getenv("SWING_FILTER_COUNTRY", "ID"),
    }


# ---------------------------------------------------------------------------
# placeholders
# ---------------------------------------------------------------------------
def render(value, **context):
    """Fill `{name}` placeholders in a str / dict / list from `context`."""
    if isinstance(value, str):
        for key, replacement in context.items():
            value = value.replace("{%s}" % key, str("" if replacement is None else replacement))
        return value
    if isinstance(value, dict):
        return {k: render(v, **context) for k, v in value.items()}
    if isinstance(value, list):
        return [render(v, **context) for v in value]
    return value


def render_url(url: str, **context) -> str:
    """Same, percent-encoded — a raw '+' in a query string would reach the
    backend as a space."""
    encoded = {k: quote(str("" if v is None else v), safe="") for k, v in context.items()}
    return render(url, **encoded)


# ---------------------------------------------------------------------------
# responses
# ---------------------------------------------------------------------------
class ApiResponse:
    """What came back, with the digging helpers a test actually wants."""

    def __init__(self, status: int, text: str, payload=None):
        self.status = status
        self.text = text
        self._payload = payload

    @property
    def ok(self) -> bool:
        return self.status < 400

    @property
    def json(self):
        """The decoded body, or None when it wasn't JSON."""
        return self._payload

    def pick(self, path: str, default=None):
        """Walk a dotted path into the body: "data.otp", "results.0.code"."""
        current = self._payload
        for part in str(path).split("."):
            if isinstance(current, list):
                if not part.lstrip("-").isdigit():
                    return default
                index = int(part)
                if not -len(current) <= index < len(current):
                    return default
                current = current[index]
            elif isinstance(current, dict):
                if part not in current:
                    return default
                current = current[part]
            else:
                return default
        return default if current is None else current

    def find(self, *keys, default=None):
        """First value under any of `keys`, at any depth — for responses whose
        shape you'd rather not pin down."""
        wanted = {k.casefold() for k in keys}

        def walk(node):
            if isinstance(node, dict):
                for actual, value in node.items():
                    if actual.casefold() in wanted and isinstance(value, (str, int, float, bool)):
                        return value
                for value in node.values():
                    found = walk(value)
                    if found is not None:
                        return found
            elif isinstance(node, list):
                for item in node:
                    found = walk(item)
                    if found is not None:
                        return found
            return None

        found = walk(self._payload)
        return default if found is None else found

    def raise_for_status(self):
        if not self.ok:
            raise ApiError(f"HTTP {self.status}: {self.text[:300]}")
        return self

    def __repr__(self):
        return f"<ApiResponse {self.status} {self.text[:80]!r}>"


# ---------------------------------------------------------------------------
# client
# ---------------------------------------------------------------------------
def _json_env(name: str):
    """Read a JSON object out of the environment; empty means 'not set'."""
    raw = os.getenv(name, "").strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ApiError(f"{name} is not valid JSON: {exc}") from exc


class ApiClient:

    def __init__(self, base_url: str = "", headers=None, params=None, body=None,
                 method: str = "GET", timeout: float = 10, retries: int = 1,
                 retry_delay: float = 3, name: str = "api"):
        self.base_url = base_url
        self.headers = headers or None
        self.params = params or None
        self.body = body or None
        self.method = method.upper()
        self.timeout = timeout
        self.retries = max(1, int(retries))
        self.retry_delay = retry_delay
        self.name = name

    # ---- construction ----
    @classmethod
    def from_env(cls, prefix: str):
        """Build a client out of {PREFIX}_URL and friends — see the module
        docstring for the full list."""
        url = (os.getenv(f"{prefix}_URL") or os.getenv(f"{prefix}_BASE_URL") or "").strip()
        if not url:
            raise ApiError(f"{prefix}_URL is not set — nothing to call")
        return cls(
            base_url=url,
            headers=_json_env(f"{prefix}_HEADERS"),
            params=_json_env(f"{prefix}_PARAMS"),
            body=_json_env(f"{prefix}_BODY"),
            method=os.getenv(f"{prefix}_METHOD", "GET"),
            timeout=float(os.getenv(f"{prefix}_TIMEOUT", "10")),
            retries=int(os.getenv(f"{prefix}_RETRIES", "1")),
            retry_delay=float(os.getenv(f"{prefix}_RETRY_DELAY", "3")),
            name=prefix.lower(),
        )

    @classmethod
    def swing(cls, **overrides) -> "ApiClient":
        """A client pointed at the Swing backend, with the app's headers.

            ApiClient.swing().request_otp("82165162549", "+62")
        """
        settings = dict(
            base_url=os.getenv("SWING_API_URL", SWING_BASE_URL).rstrip("/"),
            headers=swing_headers(),
            timeout=float(os.getenv("SWING_API_TIMEOUT", "15")),
            # Deliberately low: a retry of /otp/request sends a second real
            # WhatsApp/SMS message, so only an outright failure earns one.
            retries=int(os.getenv("SWING_API_RETRIES", "2")),
            retry_delay=float(os.getenv("SWING_API_RETRY_DELAY", "3")),
            name="swing api",
        )
        settings.update(overrides)
        return cls(**settings)

    @staticmethod
    def configured(prefix: str) -> bool:
        """True when .env points this prefix at an endpoint."""
        return bool((os.getenv(f"{prefix}_URL") or os.getenv(f"{prefix}_BASE_URL") or "").strip())

    # ---- calls ----
    def request(self, method: str = "", path: str = "", *, headers=None, params=None,
                body=None, timeout=None, retries=None, retry_delay=None,
                until=None, **context) -> ApiResponse:
        """Send one request (retrying while it fails, or while `until` says the
        answer isn't ready yet) and hand back an ApiResponse.

        `until` is a callable taking the response and returning True when the
        result is good enough to stop — that is what makes polling for a code
        the backend hasn't written yet a one-liner.
        """
        try:
            import requests
        except ImportError as exc:  # pragma: no cover - requirements pin it
            raise ApiError("the `requests` package is needed for API calls") from exc

        verb = (method or self.method).upper()
        url = render_url(self._url(path), **context)
        sent_headers = render(headers if headers is not None else self.headers, **context)
        sent_params = render(params if params is not None else self.params, **context)
        sent_body = render(body if body is not None else self.body, **context)
        timeout = self.timeout if timeout is None else timeout
        attempts = max(1, int(self.retries if retries is None else retries))
        delay = self.retry_delay if retry_delay is None else retry_delay

        last_problem = "no response"
        for attempt in range(1, attempts + 1):
            try:
                raw = requests.request(
                    verb, url, headers=sent_headers, params=sent_params,
                    json=sent_body if verb != "GET" else None, timeout=timeout,
                )
            except Exception as exc:  # network hiccup — worth another try
                last_problem = f"request failed: {exc}"
            else:
                response = self._wrap(raw)
                if not response.ok:
                    last_problem = f"HTTP {response.status}: {response.text[:200]}"
                elif until is None or until(response):
                    if attempt > 1:
                        print(f"[{self.name}] {verb} {url} ok on attempt {attempt}")
                    return response
                else:
                    last_problem = f"response not ready yet: {response.text[:200]}"

            print(f"[{self.name}] attempt {attempt}/{attempts} — {last_problem}")
            if attempt < attempts:
                time.sleep(delay)

        raise ApiError(f"{verb} {url} — {last_problem}")

    def get(self, path: str = "", **kwargs) -> ApiResponse:
        return self.request("GET", path, **kwargs)

    def post(self, path: str = "", **kwargs) -> ApiResponse:
        return self.request("POST", path, **kwargs)

    def put(self, path: str = "", **kwargs) -> ApiResponse:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str = "", **kwargs) -> ApiResponse:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str = "", **kwargs) -> ApiResponse:
        return self.request("DELETE", path, **kwargs)

    # ---- Swing endpoints ----
    def request_otp(self, phone_number: str, dial_code: str = "", method: str = "WHATSAPP",
                    spam_token: str = "", **kwargs) -> ApiResponse:
        body = {
            "phone_number": re.sub(r"\D", "", str(phone_number or "")),
            "dial_code": dial_code or os.getenv("SWING_DIAL_CODE", "+62"),
            "type": (method or "WHATSAPP").strip().upper(),
            "swing_spam_token": spam_token or os.getenv(
                "SWING_SPAM_TOKEN", "skip_swing_anti_spam"
            ),
        }
        return self.post(
            os.getenv("SWING_OTP_REQUEST_PATH", SWING_OTP_REQUEST_PATH),
            body=body, **kwargs,
        )

    # ---- internals ----
    def _url(self, path: str) -> str:
        if not path:
            return self.base_url
        if re.match(r"^https?://", path):
            return path
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    @staticmethod
    def _wrap(raw) -> ApiResponse:
        try:
            payload = raw.json()
        except ValueError:
            payload = None
        return ApiResponse(raw.status_code, raw.text, payload)


def otp_code(response: ApiResponse) -> str:
    """The login code out of an OTP response, or "" when it doesn't carry one
    (production never does — there the code only reaches the phone).

    SWING_OTP_FIELD pins the dotted path ("data.otp"); unset, any otp/code-ish
    key anywhere in the body is taken.
    """
    field = os.getenv("SWING_OTP_FIELD", "").strip()
    if response.json is None:
        text = response.text.strip().strip('"')
        return text if text.isdigit() else ""
    raw = response.pick(field) if field else response.find(*OTP_KEYS)
    return re.sub(r"\D", "", str(raw)) if raw is not None else ""
