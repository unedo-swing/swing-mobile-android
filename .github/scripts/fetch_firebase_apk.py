#!/usr/bin/env python3
"""Download the newest Android build from Firebase App Distribution.

Authenticates with a service-account key, asks the App Distribution REST API
for the most recent release of the configured app, and writes the binary to
the requested path.

Required environment:
    FIREBASE_SA_KEY           service-account JSON (the key itself, not a path)
    FIREBASE_PROJECT_NUMBER   numeric project number
    FIREBASE_ANDROID_APP_ID   e.g. 1:123456789:android:abc123

Usage:
    fetch_firebase_apk.py apps/app.apk

The release's version/build are written to $GITHUB_OUTPUT so later jobs can
cache on them and name artifacts after the build under test.
"""
import json
import os
import sys
import zipfile

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

API_ROOT = "https://firebaseappdistribution.googleapis.com/v1"
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# The CI emulator is x86_64. A Flutter release APK is often built arm64-only,
# in which case adb install fails with INSTALL_FAILED_NO_MATCHING_ABIS after
# the emulator has already booted. Cheaper to catch it here.
REQUIRED_ABI = "lib/x86_64/"


def die(message: str) -> None:
    print(f"::error::{message}", file=sys.stderr)
    sys.exit(1)


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        die(f"{name} is not set — add it to the repository secrets.")
    return value


def access_token() -> str:
    raw = require_env("FIREBASE_SA_KEY")
    try:
        info = json.loads(raw)
    except json.JSONDecodeError:
        die("FIREBASE_SA_KEY is not valid JSON — paste the whole key file.")
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    creds.refresh(Request())
    return creds.token


def latest_release(token: str) -> dict:
    project = require_env("FIREBASE_PROJECT_NUMBER")
    app_id = require_env("FIREBASE_ANDROID_APP_ID")
    url = f"{API_ROOT}/projects/{project}/apps/{app_id}/releases"
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params={"pageSize": 1, "orderBy": "createTime desc"},
        timeout=60,
    )
    if resp.status_code == 403:
        die(
            "Firebase denied the request (403). The service account needs the "
            "Firebase App Distribution Viewer role on this project."
        )
    if resp.status_code == 404:
        die(f"No such app: {app_id} in project {project}. Check the app id.")
    resp.raise_for_status()

    releases = resp.json().get("releases") or []
    if not releases:
        die(f"App Distribution has no releases for {app_id}.")
    return releases[0]


def download(uri: str, dest: str) -> None:
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    with requests.get(uri, stream=True, timeout=600) as resp:
        resp.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                fh.write(chunk)


def verify_abi(path: str) -> None:
    """Fail now, with a readable reason, if the build can't run on the emulator."""
    try:
        with zipfile.ZipFile(path) as apk:
            libs = [n for n in apk.namelist() if n.startswith("lib/")]
    except zipfile.BadZipFile:
        die(f"{path} is not a valid APK — the download may have been truncated.")

    if not libs:
        return  # no native code at all; every ABI is fine
    if not any(n.startswith(REQUIRED_ABI) for n in libs):
        abis = sorted({n.split("/")[1] for n in libs})
        die(
            f"This build ships {', '.join(abis)} but no x86_64 slice, so it "
            "cannot install on the CI emulator. Ask for a build that includes "
            "x86_64, or move the test job to a real-device farm."
        )


def emit_outputs(release: dict) -> None:
    out = os.getenv("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as fh:
        fh.write(f"version={release.get('displayVersion', 'unknown')}\n")
        fh.write(f"build={release.get('buildVersion', 'unknown')}\n")


def main() -> None:
    dest = sys.argv[1] if len(sys.argv) > 1 else "apps/app.apk"

    release = latest_release(access_token())
    version = release.get("displayVersion", "unknown")
    build = release.get("buildVersion", "unknown")
    print(f"Latest release: {version} ({build}) created {release.get('createTime')}")

    uri = release.get("binaryDownloadUri")
    if not uri:
        die("Release has no binaryDownloadUri — it may still be processing.")

    download(uri, dest)
    verify_abi(dest)
    print(f"Downloaded {os.path.getsize(dest) / 1e6:.1f} MB to {dest}")
    emit_outputs(release)


if __name__ == "__main__":
    main()
