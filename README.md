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

Every PDF is written to `reports/`. A run that reports to ClickUp uploads them
and then deletes the local copies — `PDF_CLEANUP` decides:

```bash
pytest --clickup                  # PDF_CLEANUP=uploaded — deleted once in ClickUp (default)
PDF_CLEANUP=never pytest          # always keep the files in reports/
PDF_CLEANUP=always pytest         # delete at the end of the run either way
```

With `uploaded`, a PDF that never reached ClickUp (reporting off, upload failed,
over the size cap) is kept — evidence is never lost.

### The PDF itself

Page 1 is a full-bleed cover in Swing purple (`#5C00E6`, sampled from the app's
own launcher icon) carrying the white logo, the TC ID and name, a PASS/FAIL pill
and the run's meta. Page 2 is a clickable table of contents, then one section
per step. The logos live in [assets/](assets) — extracted from the dev APK, so
they are the app's real brand assets.

## ClickUp Chat reporting

[utils/clickup_reporter.py](utils/clickup_reporter.py) posts **one message per
run** into a ClickUp channel: a status line with the counts, the run's duration,
which device / build / app state it used, **one row per test case** — TC id,
name, `PASSED`/`FAILED` and a link to that test's PDF — and then a block per
failed test with its last step, error and evidence (the same records that feed
`reports/regression_summary.txt`). Green runs post too; a channel that only ever
hears about failures gives nobody a reason to trust the silence.

```
🤖 Swing QA Automation Bot · ❌ Swing Android E2E — 1 failed · 2 passed

2026-08-19 15:40 · 4m 07s

**device**: `emulator-5554` | **target**: `dev (DEV_* from .env)` | **suite**: `regression`

**Test cases (3)**
✅ `TC001` Login with WhatsApp OTP — PASSED — [PDF](https://t90181710981.p.clickup-attachments.com/…)
✅ `TC002` Onboarding with referral code — PASSED — [PDF](…)
❌ `TC014` Book a driving range slot — FAILED — [PDF](…)
```

It is **off by default**, so a local debugging run never reaches the team:

```bash
pytest --clickup                              # this run reports
CLICKUP_REPORT=1 pytest -m regression         # every run in this environment (CI)
pytest --no-clickup                           # opt one run back out
```

Four settings in `.env` (or CI secrets) — see [.env.example](.env.example):

```bash
CLICKUP_TOKEN=pk_xxxxxxxx        # avatar -> Settings -> Apps -> API token
CLICKUP_WORKSPACE_ID=            # the number in app.clickup.com/<id>/...
CLICKUP_CHANNEL_ID=              # channel -> "..." -> Copy link, last id in the URL
CLICKUP_PDF_TASK_ID=             # the task the evidence PDFs are uploaded to
```

With any of them missing the run still finishes normally — the terminal summary
prints `ClickUp: skipped — CLICKUP_TOKEN not set` and nothing is posted. The same
goes for an HTTP error: a failing chat post prints `ClickUp: NOT posted — …` and
never changes the run's outcome.

Running under GitHub Actions the message also carries a link back to the run. To
report from the nightly workflow, set those values as repository secrets and
pass them (plus `CLICKUP_REPORT: '1'`) in the `Run Appium tests` step's `env:`.

### Who posts, and what the message says

ClickUp has **no bot account for Chat** — the v3 API posts as whoever owns the
token, and there is no Slack-style incoming webhook. For a real bot sender,
invite a dedicated user and use its token. `CLICKUP_BOT_NAME` doesn't change the
sender, it just makes the automation read as one in the channel:

```bash
CLICKUP_BOT_NAME=Swing QA Bot     # -> "🤖 Swing QA Bot · ✅ Swing Android E2E — 23 passed"
CLICKUP_BOT_ICON=🤖               # default; set empty for no icon
```

`CLICKUP_MESSAGE` replaces the whole layout with your own. `\n` is a line break,
so a multi-line template still fits on one `.env` line:

```bash
CLICKUP_MESSAGE={bot}{icon} {title} — {status}\n{passed} passed · {failed} failed in {duration} on {device}\n\n{failures}
```

Placeholders: `{bot}` `{icon}` `{title}` `{status}` `{counts}` `{passed}`
`{failed}` `{error}` `{skipped}` `{xfailed}` `{xpassed}` `{total}` `{duration}`
`{date}` `{time}` `{datetime}` `{target}` `{build}` `{package}` `{device}`
`{app_state}` `{platform}` `{suite}` `{link}` `{link_md}` `{cases}`
`{cases_count}` `{failures}` `{failures_count}`.

An unknown placeholder renders as itself (`{divice}` stays `{divice}`) so a typo
is visible in the channel rather than silently blank, and a template that can't
render at all falls back to the built-in layout — the report is never lost to a
bad format string. `CLICKUP_MESSAGE_FOOTER` adds one line under the built-in
layout without replacing it.

### Evidence PDFs in the message

ClickUp Chat has **no attachment endpoint** — a message can only carry a link.
The one upload route ClickUp documents is a task's, and it hands back a
`t<workspace>.p.clickup-attachments.com/...` URL, so the evidence PDFs are
uploaded to a host task and linked from the run message:

```bash
CLICKUP_PDF_LIST_ID=901801234567  # a List in your evidence Folder — one task per run
CLICKUP_PDF_TASK_ID=              # or one fixed task for every run (wins over the list)
CLICKUP_PDF_SCOPE=all           # all (default) | failed | off
CLICKUP_PDF_LIMIT=30            # most files one run uploads
CLICKUP_PDF_MAX_MB=25           # bigger files are skipped (ClickUp itself allows 1GB)
CLICKUP_MAX_CASES=30            # most test-case rows one message lists
```

ClickUp's hierarchy is Space > Folder > List > Task, and **only a task holds
files** — a Folder cannot, and Chat has no attachment endpoint at all. So make a
Folder for the evidence with one List in it (e.g. "QA Automation" ▸ "Android E2E
runs"), right-click the list → *Copy link* → the id is the last part of
`.../v/li/<id>`. Each run then creates its own task in that list —
`Swing Android E2E — 2026-08-19 15:44 · 1 failed · 18 passed` — attaches that
run's PDFs to it, and the message links both each file (next to its test case)
and the task itself. The Folder ends up reading as a run history.

`CLICKUP_PDF_TASK_ID` is the alternative: one fixed task every run piles its
PDFs onto. With neither id set nothing is uploaded and the rows show plain
filenames instead of links.

The whole loop for a run is: write the PDF to `reports/` → create the run's task
→ upload the PDFs to it → post the message → delete the local files
(`PDF_CLEANUP=uploaded`):

```bash
pytest -m regression --pdf --clickup
```

A failed upload is printed and skipped, never raised — the run summary reaches
the channel either way, that row just shows the filename, and the PDF stays in
`reports/` instead of being deleted. `{pdfs}`, `{pdf_url}` and `{pdf_count}` are
available to `CLICKUP_MESSAGE` too.

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
