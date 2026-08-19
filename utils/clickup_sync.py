import os
import re
import json
import time
import urllib.request

API = "https://api.clickup.com/api/v2"

STATUS_PASS = "passed"
STATUS_FAIL = "failed"


def _headers():
    tok = os.getenv("CLICKUP_TOKEN")
    if not tok:
        raise RuntimeError("CLICKUP_TOKEN not found inside .env")
    return {"Authorization": tok, "Content-Type": "application/json"}


def update_task(task_id, status=None, comment=None, pdf_url=None):
    if not task_id:
        return
    
    if pdf_url:
        req = urllib.request.Request(
            f"{API}/task/{task_id}",
            data=json.dumps(
                {"description": f"{pdf_url}"}
            ).encode(),
            headers=_headers(),
            method="PUT",
        )
        urllib.request.urlopen(req, timeout=20).read()

    if status:
        req = urllib.request.Request(
            f"{API}/task/{task_id}",
            data=json.dumps({"status": status}).encode(),
            headers=_headers(),
            method="PUT",
        )
        urllib.request.urlopen(req, timeout=20).read()

    if comment:
        req = urllib.request.Request(
            f"{API}/task/{task_id}/comment",
            data=json.dumps({"comment_text": comment}).encode(),
            headers=_headers(),
            method="POST",
        )
        urllib.request.urlopen(req, timeout=20).read()


def attach_pdf(task_id, pdf_path):
    if not task_id or not pdf_path or not os.path.exists(pdf_path):
        return ""
    tok = os.getenv("CLICKUP_TOKEN")
    if not tok:
        return ""
    boundary = "----clickupboundary7Q3k9"
    crlf = b"\r\n"
    with open(pdf_path, "rb") as fh:
        filedata = fh.read()
    body = b""
    body += b"--" + boundary.encode() + crlf
    body += (
        b'Content-Disposition: form-data; name="attachment"; filename="'
        + os.path.basename(pdf_path).encode()
        + b'"\r\n'
    )
    body += b"Content-Type: application/pdf\r\n\r\n"
    body += filedata + crlf
    body += b"--" + boundary.encode() + b"--\r\n"
    req = urllib.request.Request(
        f"{API}/task/{task_id}/attachment",
        data=body,
        headers={
            "Authorization": tok,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        raw = urllib.request.urlopen(req, timeout=30).read()
        data = json.loads(raw)
        url = data.get("url") or data.get("url_w_query") or ""
        if url:
            print(f"[clickup] PDF attached: {url}")
        else:
            print(f"[clickup] PDF attached (no url): {pdf_path}")
        return url
    except Exception as e:
        print(f"[clickup] failed to attach pdf {pdf_path}: {e}")
        return ""


def sync_results(results, mapping):
    for r in results:
        tid = mapping.get(r["tc_id"])
        if not tid:
            print(f"[clickup] tc_id '{r['tc_id']}' not found inside clickup_map.py -> skip")
            continue
        st = STATUS_PASS if r["status"] == "PASS" else STATUS_FAIL
        try:
            pdf_url = ""
            if r.get("pdf"):
                pdf_url = attach_pdf(tid, r["pdf"])
            msg = f"[{r['status']}] {r['nodeid']}"
            if r.get("error"):
                msg += f"\nError: {r['error']}"
            if pdf_url:
                msg += f"\n{pdf_url}"
            elif r.get("pdf"):
                msg += f"\n{r['pdf']}"
            update_task(tid, status=st, comment=msg, pdf_url=pdf_url)
        except Exception as e:
            print(f"[clickup] failed to sync {tid}: {e}")
        time.sleep(0.7)