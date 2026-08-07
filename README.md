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

PDFs and screenshots land in `reports/`.

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
4. Write a test in `tests/` that instantiates the flow with `(driver, pdf)`.
