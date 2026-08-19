# Swing Android — Appium + Python POM Framework

Android UI automation for the Swing app using Appium + pytest with a Page Object
Model, XPaths kept in a dedicated locator repository, and **optional PDF
evidence**. Runs on emulators and real devices.

## Structure

```
config/       capabilities.py (Android UiAutomator2 caps), settings.py
core/         driver_factory.py, base_page.py (shared actions),
              android_base_page.py (Android gestures — pages inherit this)
locators/     XPaths only — one class per screen (no logic here)
pages/        page objects — per-screen STEPS only (actions + verifications)
flows/        scenarios that compose page steps end-to-end
utils/        pdf_reporter.py — init_pdf() / generate_pdf() + the generator
              api_client.py — HTTP calls to the backend (OTP request, seeding)
assets/       Swing logos used on the PDF cover (from the dev APK)
tests/        pytest tests
apps/         app.apk (the build under test)
reports/      generated PDFs + screenshots
conftest.py   fixtures: driver, and the --pdf flag
```

## Design choices

- **Android base page.** `core/base_page.py` holds shared actions
  (find/click/type/waits/screenshots). `core/android_base_page.py` adds
  Android-only gestures (UiAutomator scroll, keyboard/permission, hardware
  back). Page objects inherit `AndroidBasePage`.
- **XPaths live in `locators/`.** Each screen is a class with plain-string XPath
  attributes. The Swing app is Flutter, so elements surface through
  `content-desc` (accessibility label) or `hint`, e.g.
  `button_continue = '//android.widget.Button[@content-desc="Continue"]'`.
  When the UI changes you edit only the locator class — never the page or test.
  The base page treats any string as an XPath automatically.
- **PDF evidence is a callable, opt-in feature.** No flag = normal run.
  `--pdf` (or `PDF_EVIDENCE=1`) = a PDF report per test. `page.capture_step()`
  records a titled screenshot; nothing extra runs when PDF is off. This is the
  "with PDF for reports / without PDF for CI on deploy" split.

## Setup

```bash
pip install -r requirements.txt
# start an emulator or plug in a real device, then start the Appium server:
appium
```

Check the device is visible: `adb devices`.

## Run

```bash
pytest                                        # no PDF  (fast — use in CI / deploy)
pytest --pdf                                  # with PDF evidence (for manual reports)
pytest tests/test_login.py::TestLogin::test_login_screen_loads --pdf
pytest -m smoke                               # only smoke tests
pytest -m "smoke and not regression"          # subset by marker
```

The PDF evidence goes **into the Allure report** — one attachment per case, no
files left in `reports/`. `PDF_OUTPUT` changes that:

```bash
pytest                            # PDF_OUTPUT=allure  — attachment only (default)
PDF_OUTPUT=reports pytest         # a file in reports/, nothing attached-only
PDF_OUTPUT=both pytest            # attached and kept as a file
```

With Allure switched off (`ALLURE=0`) the PDF always falls back to a file in
`reports/`, so evidence is never lost.

### The PDF itself

Page 1 is a full-bleed cover in Swing purple (`#5C00E6`, sampled from the app's
own launcher icon) carrying the white logo, the TC ID and name, a PASS/FAIL pill
and the run's meta. Page 2 is a clickable table of contents, then one section
per step. The logos live in [assets/](assets) — extracted from the dev APK, so
they are the app's real brand assets.

## Allure report

**Every run writes Allure results** to `reports/allure-results` — no flag
needed, the same way PDF evidence is on by default. The two are independent and
both come out of a single pass:

```bash
pytest -m regression
```

The results directory is cleared at the start of each run, so a report always
shows that run. `--allure-append` (or `ALLURE_APPEND=1`) keeps what is already
there, for splitting one logical run across several `pytest` invocations.

Rendering them needs the Allure CLI (it is a Java app, `allure-pytest` alone is
not enough):

```bash
brew install allure
```

```bash
allure serve reports/allure-results
```

What ends up in the report, with no change to any test:

* every `capture_step` becomes an Allure step with its screenshot attached;
* the case is titled from the data sheet (`TT_001 — Book standard tee time`),
  because `init_pdf(...)` passes the TC ID / TC Name through;
* feature/story come from the test module and class, severity from the marker
  (`smoke` → critical, `regression` → normal, `manual` → minor);
* every case carries its whole PDF as an attachment (under the case's
  *Tear down* section — that is where the PDF is written), and with the default
  `PDF_OUTPUT=allure` that attachment is the only copy;
* the run's target/package/device/app-state show up in the environment widget.

Turning it off and moving it:

```bash
pytest --no-allure                            # or ALLURE=0 pytest
pytest --alluredir=/tmp/results               # or ALLURE_DIR=/tmp/results pytest
pytest --allure                               # fail the run if allure-pytest is missing
```

`--allure` only forces the point: results are already on, so the flag's job is
to turn "allure-pytest isn't installed" from a silently missing report into an
error. That is why CI passes it. Without it, a machine that hasn't installed the
package still runs the suite — the header line says `allure: OFF`.

`ALLURE_TMS_URL="https://tms.example.com/case/{tc_id}"` turns each TC ID into a
link on its case (no link when unset).

`allure serve` renders a one-off report — for trends across runs, keep the
previous report's `history/` folder and use `allure generate --clean`.

## Calling an API from a test

[utils/api_client.py](utils/api_client.py) is the one HTTP helper — requesting
an OTP, seeding data, checking what the backend really stored after a booking.
`ApiClient.swing()` is the Swing backend with the headers the app sends
(`x-api-key`, `X-Device`, `X-Device-Id`, `X-SOURCE`, …, all overridable via
`SWING_*` in `.env`); other APIs come from an env prefix or from code:

```python
from utils.api_client import ApiClient, otp_code

swing = ApiClient.swing()
code = otp_code(swing.request_otp("82165162549", "+62", "WHATSAPP"))

# BOOKING_API_URL / _HEADERS / _RETRIES / ... in .env
api = ApiClient.from_env("BOOKING_API")

# or inline
api = ApiClient("https://api-dev.getswing.cloud", headers={"Authorization": f"Bearer {token}"})

booking = api.get("/v1/bookings/{id}", id=booking_id)
assert booking.pick("data.status") == "CONFIRMED"
```

`{name}` placeholders are filled from the call's keyword arguments (url-encoded
in the URL) and work in the path, headers, query params and body. On the
response, `.pick("data.status")` walks a dotted path (`results.0.code` too) and
`.find("status")` grabs the first match at any depth. `retries=` /
`until=lambda r: ...` poll an endpoint that isn't ready yet; a failed call
raises `ApiError`. The seven env keys per prefix are listed in `.env.example`.

### OTP from the API

`request_otp()` posts to `/players/api/v1/auth/otp/request` — the same call the
app makes when Continue is tapped — and `otp_code(response)` pulls the code out
of the answer, so a blank `OTP` cell no longer means someone has to read a
phone. `SWING_OTP_FIELD` pins the dotted path to the code (unset = the first
`otp`/`code`-ish key wins).

The dial code comes from the app, not the test data: `select_country()` reads
the country button (`ID (+62)`) and keeps `+62` for the request, so changing the
`COUNTRY` column is enough. `SWING_DIAL_CODE` (default `+62`) covers the case
where the button can't be read, and `login_with_otp(..., dial_code="+355")`
forces a different one.

Where the code comes from, in order:

| `OTP` cell | Result |
| --- | --- |
| `api` or `auto` | hits the endpoint; fails the test if it answers without a code |
| `000000`, any value | uses the cell (bypass code) — no API call |
| blank | hits the endpoint, then asks at the terminal if no code came back |

## Real device vs emulator

Same code — only the target changes, via env vars (no file edits):

```bash
# emulator (default)
DEVICE_NAME=emulator-5554 pytest

# real device (get the serial from `adb devices`)
DEVICE_NAME=RZ8N70XXXXX pytest
```

## Add a new screen

1. `locators/<screen>_locators.py` — a `class <Screen>Locators` with plain XPath
   string attributes (prefer `content-desc` / `resource-id` / `hint`).
2. `pages/<screen>_page.py` — a class extending `AndroidBasePage`, importing that
   locator class, with `fill / tap / verify` methods that call `capture_step`.
3. `flows/<screen>_flow.py` — compose the page steps into scenarios.
4. `conftest.py` — add a fixture for the flow: `return flow(<Screen>Flow)`.
5. Write a test in `tests/` that takes that fixture, opens its report with
   `pdf = init_pdf("<test name>")` on the first line, and closes it with
   `generate_pdf(pdf)` after the last step.
