import os

import pytest

from config import settings
from utils.pdf_reporter import (
    active_pdf_path,
    active_reporter,
    evidence_written,
    generate_pdf,
    reset_evidence,
)


def _record_failure(request, pdf, rep, evidence):
    last = pdf.steps[-1] if (pdf is not None and pdf.steps) else None
    shot = last["screenshot"] if last else None
    message = ""
    if rep.longrepr is not None:
        crash = getattr(rep.longrepr, "reprcrash", None)
        message = (crash.message if crash is not None else str(rep.longrepr)) or ""
    request.config._regression_failures.append({
        "test": request.node.nodeid,
        "phase": rep.when,  # "setup" or "call"
        "last_step": last["title"] if last else "(no steps captured)",
        "last_description": last["description"] if last else "",
        "last_screenshot": os.path.basename(shot) if shot else None,
        "pdf": evidence,
        "error": message.strip().splitlines()[0] if message.strip() else "",
    })


def _empty_screenshots_dir():
    folder = settings.SCREENSHOTS_DIR
    if not os.path.isdir(folder):
        return
    for name in os.listdir(folder):
        fp = os.path.join(folder, name)
        try:
            if os.path.isfile(fp):
                os.remove(fp)
        except OSError:
            pass  # best-effort cleanup; never fail a test over this

@pytest.fixture(autouse=True)
def pdf_evidence(request):
    reset_evidence()
    yield

    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    failed_rep = next(
        (r for r in (rep_setup, rep_call) if r is not None and r.failed), None
    )
    pdf = active_reporter()
    pdf_path = active_pdf_path()
    if failed_rep is not None and not evidence_written():
        pdf_path = generate_pdf(pdf, status="FAIL")
    # screenshots are embedded in the PDF now -> clear the folder once it's built
    if pdf_path:
        _empty_screenshots_dir()
    # the ClickUp reporter uploads these at the end of the run and links each one
    # next to its test case, then deletes the local file (see PDF_CLEANUP)
    on_disk = pdf_path if (pdf_path and os.path.exists(pdf_path)) else None
    if on_disk:
        request.config._run_pdfs.append(on_disk)
    skipped = any(r is not None and r.skipped for r in (rep_setup, rep_call))
    request.config._run_results.append({
        "test": request.node.nodeid,
        "tc_id": getattr(pdf, "tc_id", "") or "",
        "name": (getattr(pdf, "tc_name", "") or getattr(pdf, "test_name", "")
                 or request.node.name),
        "status": "FAILED" if failed_rep is not None else ("SKIPPED" if skipped else "PASSED"),
        "pdf": on_disk,
    })
    if failed_rep is not None:
        _record_failure(request, pdf, failed_rep, on_disk)
