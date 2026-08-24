import json
import os
from datetime import datetime

try:  # requests is in requirements.txt; degrade instead of breaking a run
    import requests
    AVAILABLE = True
except ImportError:  # pragma: no cover - depends on the environment
    requests = None
    AVAILABLE = False


API_BASE = os.getenv("CLICKUP_API_BASE", "https://api.clickup.com/api")
MESSAGE_PATHS = (
    "/v3/workspaces/{workspace}/chat/channels/{channel}/messages",
    "/v3/workspaces/{workspace}/channels/{channel}/messages",
)

# In ClickUp's hierarchy (Space > Folder > List > Task) only a task holds files
# — a Folder cannot, and Chat has no attachment endpoint at all. So the evidence
# needs a task, and there are two ways to give it one:
#   CLICKUP_PDF_LIST_ID  a List inside your evidence Folder: every run creates
#                        its own task there and attaches that run's PDFs
#   CLICKUP_PDF_TASK_ID  one fixed task every run piles its PDFs onto (wins
#                        over the list when both are set)
ATTACHMENT_PATH = "/v2/task/{task}/attachment"
TASK_PATH = "/v2/list/{list}/task"

# ClickUp rejects very long messages; keep well under it and cap both lists so a
# 40-test, 40-failure run still posts something readable.
MAX_MESSAGE_CHARS = 9000
MAX_FAILURES_LISTED = 10
MAX_CASES_LISTED = int(os.getenv("CLICKUP_MAX_CASES", "30"))

# The row of a test case, by status.
STATUS_ICONS = {"PASSED": "✅", "FAILED": "❌", "SKIPPED": "⏭️"}

TIMEOUT = int(os.getenv("CLICKUP_TIMEOUT", "15"))
# Uploads are slower than a message — a 20MB evidence PDF needs its own budget.
UPLOAD_TIMEOUT = int(os.getenv("CLICKUP_UPLOAD_TIMEOUT", "120"))


def enabled(config) -> bool:
    """True when this run should report — ``--clickup`` or CLICKUP_REPORT=1.

    ``--collect-only`` never reports: it runs no test, so it has nothing to say
    and would post an empty report over the last real one.
    """
    from config import settings

    if config is None:
        return bool(settings.CLICKUP_REPORT)
    if config.getoption("no_clickup", False) or config.getoption("collectonly", False):
        return False
    return bool(settings.CLICKUP_REPORT or config.getoption("clickup", False))


def credentials() -> dict:
    """Token + ids, read at send time so .env changes need no restart."""
    return {
        "token": os.getenv("CLICKUP_TOKEN", "").strip(),
        "workspace": os.getenv("CLICKUP_WORKSPACE_ID", "").strip(),
        "channel": os.getenv("CLICKUP_CHANNEL_ID", "").strip(),
    }


def missing_credentials(creds: dict) -> list:
    """Which of the three required settings are not set."""
    names = {
        "token": "CLICKUP_TOKEN",
        "workspace": "CLICKUP_WORKSPACE_ID",
        "channel": "CLICKUP_CHANNEL_ID",
    }
    return [names[key] for key, value in creds.items() if not value]


# --------------------------------------------------------------------------- #
# evidence PDFs
# --------------------------------------------------------------------------- #
def _pdf_settings() -> dict:
    """Which PDFs to upload, and the limits — all from .env."""
    return {
        "task": os.getenv("CLICKUP_PDF_TASK_ID", "").strip(),
        "list": os.getenv("CLICKUP_PDF_LIST_ID", "").strip(),
        # "all" (default) uploads every PDF the run wrote, so each test case in
        # the message carries its own evidence link; "failed" uploads only the
        # failures' evidence; "off" uploads nothing.
        "scope": os.getenv("CLICKUP_PDF_SCOPE", "all").strip().lower(),
        "limit": int(os.getenv("CLICKUP_PDF_LIMIT", "30")),
        "max_mb": float(os.getenv("CLICKUP_PDF_MAX_MB", "25")),
    }


def _pdfs_to_upload(summary: dict, config: dict) -> list:
    """The PDF files this run should upload, honouring scope and the size cap."""
    if config["scope"] == "failed":
        paths = [f.get("pdf") for f in (summary.get("failures") or [])]
    else:
        paths = list(summary.get("pdfs") or [])

    chosen, seen = [], set()
    for path in paths:
        if not path or path in seen or not os.path.isfile(path):
            continue
        seen.add(path)
        if os.path.getsize(path) > config["max_mb"] * 1024 * 1024:
            print(f"[clickup] {os.path.basename(path)} skipped — over {config['max_mb']}MB")
            continue
        chosen.append(path)
        if len(chosen) >= config["limit"]:
            break
    return chosen


def _run_task_name(summary: dict) -> str:
    """'Swing Android E2E — 2026-08-19 15:44 · 1 failed · 18 passed'."""
    title = summary.get("title") or "Android E2E"
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"{title} — {stamp} · {_counts_line(summary.get('counts') or {})}"


def host_task(summary: dict, creds: dict, config: dict) -> tuple:
    """The task this run's PDFs are attached to, as (id, url).

    A fixed CLICKUP_PDF_TASK_ID is used as-is. Otherwise, with
    CLICKUP_PDF_LIST_ID set, the run creates its own task in that list — one
    task per run, so the evidence Folder reads as a run history instead of a
    single task with hundreds of files. ('', '') when neither is configured or
    the task could not be created: the run then reports without links and keeps
    its PDFs on disk.
    """
    if config["task"]:
        return config["task"], ""
    if not config["list"]:
        return "", ""

    meta = summary.get("metadata") or {}
    body = "\n".join(
        f"{label}: {meta[key]}"
        for label, key in (("device", "device"), ("target", "target"),
                           ("build", "apk"), ("package", "package"))
        if meta.get(key)
    )
    try:
        response = requests.post(
            API_BASE.rstrip("/") + TASK_PATH.format(list=config["list"]),
            headers={
                "Authorization": creds["token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            data=json.dumps({
                "name": _run_task_name(summary),
                "description": body or "Automation evidence.",
            }),
            timeout=TIMEOUT,
        )
    except Exception as exc:
        print(f"[clickup] evidence task not created — {type(exc).__name__}: {exc}")
        return "", ""
    if response.status_code >= 300:
        print(f"[clickup] evidence task not created — HTTP {response.status_code} "
              f"{response.text[:150]}")
        return "", ""
    task = response.json() or {}
    return task.get("id", ""), task.get("url", "")


def upload_pdfs(summary: dict, creds: dict) -> tuple:
    config = _pdf_settings()
    if config["scope"] == "off":
        return [], ""
    files = _pdfs_to_upload(summary, config)
    if not files:
        return [], ""

    # only worth creating a task once there is something to put on it
    task, task_url = host_task(summary, creds, config)
    if not task:
        return [], ""

    uploaded = []
    for path in files:
        name = os.path.basename(path)
        try:
            with open(path, "rb") as fh:
                response = requests.post(
                    API_BASE.rstrip("/") + ATTACHMENT_PATH.format(task=task),
                    headers={"Authorization": creds["token"]},
                    files={"attachment": (name, fh, "application/pdf")},
                    timeout=UPLOAD_TIMEOUT,
                )
        except Exception as exc:
            print(f"[clickup] upload failed for {name} — {type(exc).__name__}: {exc}")
            continue
        if response.status_code >= 300:
            print(f"[clickup] upload failed for {name} — HTTP {response.status_code} "
                  f"{response.text[:150]}")
            continue
        url = (response.json() or {}).get("url", "")
        if url:
            uploaded.append({"path": path, "name": name, "url": url})
        else:
            print(f"[clickup] {name} uploaded but the response carried no url")
    return uploaded, task_url


def _pdf_block(uploaded: list) -> str:
    """'**Automation PDF Report**' plus one link per uploaded file.

    A fallback listing: with the per-test-case rows in the message every PDF is
    already linked next to its test, so the built-in layout only falls back to
    this when the run recorded no cases at all.
    """
    if not uploaded:
        return ""
    if len(uploaded) == 1:
        item = uploaded[0]
        return f"**Automation PDF Report**: [{item['name']}]({item['url']})"
    lines = ["**Automation PDF Report**"]
    lines += [f"- [{item['name']}]({item['url']})" for item in uploaded]
    return "\n".join(lines)


def cleanup_pdfs(paths, links: dict) -> int:
    """Delete the local evidence PDFs the run no longer needs to keep.

    ``links`` is {local path: ClickUp url} — with the default
    PDF_CLEANUP=uploaded only files in there are removed, so evidence that never
    reached ClickUp (reporting off, upload failed, over the size cap) stays on
    disk. Best-effort: a file that refuses to go is left alone, never raised.
    """
    from config import settings

    mode = settings.PDF_CLEANUP
    if mode == "never":
        return 0

    removed = 0
    for path in dict.fromkeys(paths or []):
        if mode == "uploaded" and path not in (links or {}):
            continue
        try:
            os.remove(path)
            removed += 1
        except OSError as exc:
            print(f"[evidence] could not remove {os.path.basename(path)} — {exc}")
    if removed:
        where = "uploaded to ClickUp and removed" if mode == "uploaded" else "removed"
        print(f"[evidence] {removed} PDF(s) {where} from reports/")
    return removed


def _cases_block(results: list, links: dict) -> str:
    """One row per test case — the run report itself.

        ✅ `TC001` Login with WhatsApp OTP — PASSED — [PDF](https://…)

    The TC id sits in code ticks because ClickUp reads the underscores in an id
    like TC_01 as Markdown emphasis and eats them.
    """
    if not results:
        return ""
    lines = [f"**Test cases ({len(results)})**"]
    for case in results[:MAX_CASES_LISTED]:
        status = case.get("status") or "?"
        parts = [STATUS_ICONS.get(status, "•")]
        if case.get("tc_id"):
            parts.append(f"`{case['tc_id']}`")
        parts.append(case.get("name") or case.get("test") or "?")
        row = f"{' '.join(parts)} — {status}"
        path = case.get("pdf")
        url = (links or {}).get(path) if path else ""
        if url:
            row += f" — [PDF]({url})"
        elif path:
            row += f" — {os.path.basename(path)}"
        lines.append(row)
    left = len(results) - MAX_CASES_LISTED
    if left > 0:
        lines.append(f"…and {left} more")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# the message
# --------------------------------------------------------------------------- #
def _duration(seconds) -> str:
    """'6m 12s' / '48s' — None when the run length isn't known."""
    if not seconds or seconds < 0:
        return ""
    seconds = int(seconds)
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m {secs}s" if minutes else f"{secs}s"


def _counts_line(counts: dict) -> str:
    """'3 failed · 20 passed · 1 skipped' — only the non-zero buckets."""
    order = ("failed", "error", "passed", "skipped", "xfailed", "xpassed")
    parts = [f"{counts.get(key, 0)} {key}" for key in order if counts.get(key)]
    return " · ".join(parts) or "no tests ran"


def _run_link() -> str:
    """A link back to the CI run when this is GitHub Actions; '' locally."""
    server = os.getenv("GITHUB_SERVER_URL", "").rstrip("/")
    repo = os.getenv("GITHUB_REPOSITORY", "")
    run_id = os.getenv("GITHUB_RUN_ID", "")
    if server and repo and run_id:
        return f"{server}/{repo}/actions/runs/{run_id}"
    return ""


def _sender() -> str:
    """The 'who is talking' prefix — '🤖 **Swing QA Bot** · ', or '' when unset.

    ClickUp has no bot identity for Chat: whatever token posts, the message is
    attributed to that user. CLICKUP_BOT_NAME doesn't change that, it only makes
    the automation read as an automation in the channel.
    """
    name = os.getenv("CLICKUP_BOT_NAME", "").strip()
    if not name:
        return ""
    icon = os.getenv("CLICKUP_BOT_ICON", "🤖").strip()
    return f"{icon} **{name}** · " if icon else f"**{name}** · "


def _failure_block(failures: list, links: dict = None) -> str:
    """The failed tests, one numbered block each — '' for a clean run."""
    if not failures:
        return ""
    lines = [f"**Failures ({len(failures)})**"]
    for index, failure in enumerate(failures[:MAX_FAILURES_LISTED], start=1):
        lines.append(f"{index}. `{failure.get('test', '?')}` (in {failure.get('phase', '?')})")
        lines.append(f"    - last step: {failure.get('last_step') or '(no steps captured)'}")
        if failure.get("error"):
            lines.append(f"    - error: {failure['error']}")
        path = failure.get("pdf")
        if path:
            # the local file is deleted once it is in ClickUp — link that copy
            url = (links or {}).get(path)
            lines.append(f"    - evidence: [{os.path.basename(path)}]({url})" if url
                         else f"    - evidence: {path}")
    left = len(failures) - MAX_FAILURES_LISTED
    if left > 0:
        lines.append(f"…and {left} more — see reports/regression_summary.txt")
    return "\n".join(lines)


class _Fields(dict):
    """Placeholders for a custom template. An unknown one renders as itself
    ('{divice}' stays '{divice}') so a typo shows up in the channel instead of
    silently blanking out — and never raises mid-run."""

    def __missing__(self, key):
        return "{" + key + "}"


def fields(summary: dict) -> dict:
    """Every placeholder CLICKUP_MESSAGE can use, ready-rendered."""
    counts = summary.get("counts") or {}
    failures = summary.get("failures") or []
    results = summary.get("results") or []
    meta = summary.get("metadata") or {}
    uploaded = summary.get("uploaded") or []
    links = summary.get("links") or {}
    task_url = summary.get("task_url") or ""
    broken = counts.get("failed", 0) + counts.get("error", 0)
    now = datetime.now()
    link = _run_link()

    return _Fields({
        "bot": _sender(),
        "icon": "❌" if broken else ("✅" if counts.get("passed") else "⚠️"),
        "title": summary.get("title") or "Android E2E",
        "status": "FAILED" if broken else ("PASSED" if counts.get("passed") else "NO TESTS"),
        "counts": _counts_line(counts),
        "passed": counts.get("passed", 0),
        "failed": counts.get("failed", 0),
        "error": counts.get("error", 0),
        "skipped": counts.get("skipped", 0),
        "xfailed": counts.get("xfailed", 0),
        "xpassed": counts.get("xpassed", 0),
        "total": sum(counts.values()),
        "duration": _duration(summary.get("duration")),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "datetime": now.strftime("%Y-%m-%d %H:%M"),
        "target": meta.get("target", ""),
        "build": meta.get("apk", ""),
        "package": meta.get("package", ""),
        "device": meta.get("device", ""),
        "app_state": meta.get("app state", ""),
        "platform": meta.get("platform", ""),
        "suite": summary.get("marker") or "all tests",
        "link": link,
        "link_md": f"[CI run]({link})" if link else "",
        "cases": _cases_block(results, links),
        "cases_count": len(results),
        "failures": _failure_block(failures, links),
        "failures_count": len(failures),
        "task_url": task_url,
        "task_md": (f"**Evidence**: [all {len(uploaded)} PDFs of this run]({task_url})"
                    if (task_url and uploaded) else ""),
        "pdfs": _pdf_block(uploaded),
        "pdf_url": uploaded[0]["url"] if uploaded else "",
        "pdf_count": len(uploaded),
    })


def _default_message(values: dict) -> str:
    """The built-in layout: status line, run context, then the failures."""
    # values go in code ticks: ClickUp otherwise turns "app.getswing.dev" into a
    # link and eats the underscores in "DEV_*" as Markdown emphasis
    context = [
        f"**{label}**: `{values[key]}`"
        for label, key in (
            ("device", "device"),
            ("target", "target"),
            ("build", "build"),
            ("package", "package"),
            ("app state", "app_state"),
            ("suite", "suite"),
        )
        if values.get(key)
    ]

    lines = [
        f"{values['bot']}{values['icon']} **{values['title']}** — {values['counts']}",
        "",
        " · ".join(part for part in (values["datetime"], values["duration"]) if part),
    ]
    if context:
        lines += ["", " | ".join(context)]
    if values["link_md"]:
        lines += ["", values["link_md"]]
    if values["cases"]:
        lines += ["", values["cases"]]
    if values["task_md"]:
        lines += ["", values["task_md"]]
    if values["failures"]:
        lines += ["", values["failures"]]
    # every case row already carries its own link — the flat list is only for a
    # run that reported no cases at all
    if values["pdfs"] and not values["cases"]:
        lines += ["", values["pdfs"]]

    footer = os.getenv("CLICKUP_MESSAGE_FOOTER", "").strip()
    if footer:
        lines += ["", footer.replace("\\n", "\n")]
    return "\n".join(lines)


def build_message(summary: dict) -> str:
    """Render the run as the Markdown that goes into the channel.

    ``summary`` is what conftest collects:
        title     str  — e.g. "Swing Android E2E"
        counts    dict — passed/failed/error/skipped/xfailed/xpassed
        duration  float seconds (optional)
        metadata  dict — the run header (target, package, device, app state, ...)
        results   list — one {tc_id, name, status, pdf} per test case
        failures  list — the regression-summary records
        marker    str  — the -m expression the run used (optional)

    Set CLICKUP_MESSAGE to write the whole message yourself, out of the
    placeholders in fields() — ``\\n`` in that variable becomes a line break, so
    a multi-line template still fits on one .env line:

        CLICKUP_MESSAGE={bot}{icon} {title} — {status}\\n{passed} passed, {failed}
        failed in {duration} on {device}\\n{failures}

    A template that renders empty falls back to the built-in layout, so a typo
    can't turn the report into a blank message.
    """
    values = fields(summary)

    template = os.getenv("CLICKUP_MESSAGE", "").strip()
    message = ""
    if template:
        try:
            message = template.replace("\\n", "\n").format_map(values).strip()
        except (ValueError, IndexError, KeyError, TypeError) as exc:
            # a stray brace or a format spec the value can't take — report the
            # run anyway rather than losing it to a broken template
            print(f"[clickup] CLICKUP_MESSAGE ignored ({type(exc).__name__}: {exc})")
    if not message:
        message = _default_message(values)

    if len(message) > MAX_MESSAGE_CHARS:
        message = message[: MAX_MESSAGE_CHARS - 20].rstrip() + "\n…(truncated)"
    return message


# --------------------------------------------------------------------------- #
# posting
# --------------------------------------------------------------------------- #
def _post(path: str, creds: dict, payload: dict):
    url = API_BASE.rstrip("/") + path.format(
        workspace=creds["workspace"], channel=creds["channel"]
    )
    return requests.post(
        url,
        headers={
            "Authorization": creds["token"],
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        data=json.dumps(payload),
        timeout=TIMEOUT,
    )


def send(summary: dict) -> tuple:
    """Upload the evidence, then post the run summary to the configured channel.

    Returns ``(line, links)``: a one-line result for the terminal — what was
    posted, or why it wasn't — and {local pdf path: ClickUp url} for every file
    that made it up, which is what conftest prints and what ``cleanup_pdfs`` is
    allowed to delete. Never raises: a broken chat post must not turn a green
    run red, and it must never cost the run its evidence.
    """
    if not AVAILABLE:
        return ("ClickUp: skipped — requests is not installed "
                "(pip install -r requirements.txt)"), {}

    creds = credentials()
    missing = missing_credentials(creds)
    if missing:
        return f"ClickUp: skipped — {', '.join(missing)} not set", {}

    # evidence first: the links have to exist before the message that carries them
    uploaded, task_url = upload_pdfs(summary, creds)
    links = {item["path"]: item["url"] for item in uploaded}
    summary = dict(summary, uploaded=uploaded, links=links, task_url=task_url)

    payload = {"type": "message", "content_format": "text/md", "content": build_message(summary)}

    override = os.getenv("CLICKUP_MESSAGES_PATH", "").strip()
    paths = (override,) if override else MESSAGE_PATHS

    last = ""
    for path in paths:
        try:
            response = _post(path, creds, payload)
        except Exception as exc:  # network down, DNS, timeout — report, never raise
            last = f"{type(exc).__name__}: {exc}"
            continue
        if response.status_code < 300:
            return f"ClickUp: run summary posted to channel {creds['channel']}", links
        last = f"HTTP {response.status_code} — {response.text[:200]}"
        # only a wrong path is worth retrying; a bad token or id fails the same
        # way on every path
        if response.status_code != 404:
            break
    return f"ClickUp: NOT posted — {last}", links
