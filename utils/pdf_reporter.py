"""
PDF evidence generator.

This is fully optional. When PDF evidence is enabled a ``PDFReporter`` is
created per test and passed into the page objects; each ``capture_step`` adds a
titled screenshot. At the end of the test ``generate()`` builds the PDF.

Steps can carry structured data:
  * ``data``    -> a dict rendered as a "list-down" Field/Value table.
  * ``compare`` -> {left_label, right_label, before, after, mismatch_fields}
                   rendered as a side-by-side (left vs right) table, mismatches
                   highlighted in red.

Layout — the same report the iOS suite produces
(SWING_APPS_IOS/helpers/pdf_report.py), drawn here with reportlab:
  * Page 1  -> cover: full-bleed Swing purple, the white wordmark, the company
               and department, "AUTOMATION REPORT", the scenario, the failure
               reason when the run failed, and the reporting-by / tools block.
  * Page 2+ -> "Table of Content": one numbered, clickable line per step with
               the page it lands on — real page numbers, computed with a first
               "measurement" pass over the same content (afterFlowable hook)
               before the final PDF is rendered.
  * then    -> the scenario summary: scenario, meta block (steps, application
               id, status, platform, execution start / end / time, host) the
               failure box when it failed, and the No / Test Step / Status
               table.
  * then    -> "TEST CASE EVIDENCE IMAGE": every step, its screenshot and its
               "Desc : [PASSED]" line, plus any data / compare table.
  * Every page after the cover carries the company header and the footer band
               with "Page X".

When PDF evidence is disabled no reporter is created, page objects receive
``None``, and nothing here runs — the automation runs exactly the same, just
without a PDF.
"""
import getpass
import io
import os
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    SimpleDocTemplate,
    CondPageBreak,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
)

from config import settings


# Feature prefixes used in capture_step slugs -> readable labels.
_FEATURE_PREFIXES = {"dr": "Driving Range", "tt": "Tee Time"}

# --- report identity (same wording as the iOS report) --------------------- #
COMPANY = "PT Silverwing Wisteria Indosport"
DEPARTMENT = "Dept. QA Automation Swing"
REPORT_LABEL = "Appium Report Testing"
REPORTING_BY = "Automation Team Swing"
TOOLS = "Appium - Python"
FOOTER_TEXT = "AUTOMATION TESTING REPORT - PT SILVERWING WISTERIA INDOSPORT"

# --- brand ---------------------------------------------------------------- #
BRAND = colors.Color(92 / 255, 0, 229 / 255)
BRAND_TINT = colors.Color(226 / 255, 214 / 255, 253 / 255)
INK = colors.Color(33 / 255, 33 / 255, 33 / 255)
GREY = colors.Color(110 / 255, 110 / 255, 110 / 255)
LINE = colors.Color(196 / 255, 196 / 255, 196 / 255)
BAND = colors.Color(238 / 255, 240 / 255, 245 / 255)
PASS_COLOR = colors.Color(26 / 255, 143 / 255, 68 / 255)
FAIL_COLOR = colors.Color(198 / 255, 40 / 255, 40 / 255)
FAIL_WASH = colors.Color(253 / 255, 236 / 255, 236 / 255)
FAIL_RED_HEX = "#C62828"
PASS_GREEN_HEX = "#1A8F44"
BRAND_HEX = "#5C00E5"

_ASSETS_DIR = os.path.join(settings.BASE_DIR, "assets")
# Purple wordmark on transparency — the header of every white page.
LOGO = os.path.join(_ASSETS_DIR, "swing_report_logo.png")
# White wordmark — the purple cover.
LOGO_WHITE = os.path.join(_ASSETS_DIR, "swing_report_logo_white.png")
_LOGO_RATIO = 64 / 214  # both wordmarks are 214 x 64

# --- geometry (mirrors the iOS report's millimetre grid) ------------------ #
MARGIN = 18 * mm
HEADER_H = 34 * mm
FOOTER_H = 20 * mm
IMAGE_MAX_H = 190 * mm
TABLE_IMAGE_H = 100 * mm
IMAGE_MAX_W = 150 * mm
CONTENT_W = A4[0] - 2 * MARGIN
CONTENT_H = A4[1] - HEADER_H - FOOTER_H - 6 * mm


def _y(top: float) -> float:
    """Millimetre-from-the-top coordinates, the way the iOS report is laid out,
    turned into reportlab's from-the-bottom y."""
    return A4[1] - top


def _step_failed(step: dict) -> bool:
    return (step.get("status") or "").upper() == "FAIL"


def _step_status(step: dict) -> str:
    return "FAILED" if _step_failed(step) else "PASSED"


def _elapsed(seconds: float) -> str:
    total = int(seconds or 0)
    return f"{total // 3600:02d}:{total % 3600 // 60:02d}:{total % 60:02d}"


def humanize_step(slug: str) -> str:
    """Turn a capture_step slug into a readable title.

    'dr_booking_id'        -> 'Driving Range: Booking id'
    'driving_range_explore'-> 'Driving range explore'
    """
    slug = (slug or "").strip()
    if not slug:
        return "Step"
    parts = slug.split("_")
    feature = ""
    if parts[0] in _FEATURE_PREFIXES:
        feature = _FEATURE_PREFIXES[parts[0]]
        parts = parts[1:]
    label = " ".join(parts).replace("-", " ").strip()
    label = label[:1].upper() + label[1:] if label else ""
    if feature and label:
        return f"{feature}: {label}"
    return feature or label or slug


def _parse_kv(description: str) -> dict | None:
    """Parse a 'k=v | k=v | ...' description into a dict, else None.

    Lets existing summary steps (which join fields with ' | ') render as a
    Field/Value table without changing the page code. Only multi-field lines
    (joined with '|') are parsed, so a single 'x = y' caption stays plain text.
    """
    if not description or "|" not in description or "=" not in description:
        return None
    data = {}
    for part in description.split("|"):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            return None  # not a pure key=value line — leave as plain text
        key, value = part.split("=", 1)
        data[key.strip()] = value.strip()
    return data or None


class _TrackingDocTemplate(SimpleDocTemplate):
    """SimpleDocTemplate that records which page each bookmarked step flowable
    lands on. Used for a first, throwaway "measurement" pass so the real build
    can render a Table of content with accurate page numbers — the standard
    two-pass technique reportlab's own TableOfContents/multiBuild uses
    internally, done by hand here so we control the layout."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bookmark_pages: dict[str, int] = {}
        # last page that actually had a flowable drawn on it — NOT the same as
        # canv.getPageNumber() at the very end of build(), which can count one
        # extra "phantom" page that showPage() opened but nothing was ever
        # drawn on, and that never makes it into the saved PDF.
        self.last_content_page = 1

    def afterFlowable(self, flowable):
        page = self.canv.getPageNumber()
        self.last_content_page = max(self.last_content_page, page)
        bookmark = getattr(flowable, "_toc_bookmark", None)
        if bookmark:
            self.bookmark_pages[bookmark] = page


class PDFReporter:
    def __init__(self, test_name: str, platform: str,
                 tc_id: str | None = None, tc_name: str | None = None):
        self.test_name = test_name
        self.platform = platform
        self.started_at = datetime.now()
        self.steps: list[dict] = []
        # Best-effort guess from pytest's parametrize id; call set_test_case()
        # once the real data-sheet row is loaded for an accurate cover page.
        self.tc_id = tc_id or self._derive_tc_id(test_name)
        self.tc_name = tc_name or ""
        self.error = ""

    @staticmethod
    def _derive_tc_id(test_name: str) -> str:
        """'test_book_standard_tee_time_full[TT_001]' -> 'TT_001'; '' if the
        test isn't parametrized."""
        if "[" in test_name and test_name.endswith("]"):
            return test_name[test_name.rindex("[") + 1: -1]
        return ""

    def set_test_case(self, tc_id: str | None = None, tc_name: str | None = None):
        """Override the cover page's TC ID / TC Name. Call this once the data
        sheet row is loaded (e.g. right after ``D.load(TC_ID)``) — the
        constructor only has pytest's parametrize id to guess from, and has no
        way to know the sheet's TC_NAME column."""
        if tc_id:
            self.tc_id = tc_id
        if tc_name:
            self.tc_name = tc_name

    def add_step(self, title: str, description: str = "", screenshot: str | None = None,
                 data: dict | None = None, compare: dict | None = None,
                 status: str = ""):
        self.steps.append(
            {
                "title": title,
                "description": description,
                "screenshot": screenshot,
                "data": data,
                "compare": compare,
                "status": status,
                "time": datetime.now(),
            }
        )

    # ------------------------------------------------------------------ #
    # Identity
    # ------------------------------------------------------------------ #
    def scenario(self) -> str:
        """'TT_001 Standard booking' — what the cover and summary call the run."""
        name = self.tc_name or self.test_name
        return f"{self.tc_id} {name}".strip() if self.tc_id else str(name)

    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def generate(self, status: str = "", output_dir: str | None = None,
                 error: str = "") -> str:
        """Render the collected steps into a PDF and return its file path."""
        output_dir = output_dir or settings.REPORTS_DIR
        os.makedirs(output_dir, exist_ok=True)

        if error:
            self.error = error
        self.finished_at = datetime.now()

        stamp = self.started_at.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.test_name}_{self.platform}_{stamp}.pdf"
        path = os.path.join(output_dir, filename)

        doc_kwargs = dict(
            pagesize=A4,
            topMargin=HEADER_H, bottomMargin=FOOTER_H + 6 * mm,
            leftMargin=MARGIN, rightMargin=MARGIN,
            title=self.scenario(),
        )

        styles = getSampleStyleSheet()
        self._styles = self._build_styles(styles)
        self._cell_style = self._styles["cell"]
        self._cell_bold = self._styles["cell_bold"]
        self._status = (status or "").upper()

        # NOTE: flowables must be freshly built for EACH pass — reportlab
        # Image/Paragraph flowables are not safe to reuse across two separate
        # doc.build() calls (confirmed empirically: reusing the same objects
        # makes the second build misjudge available frame space and raise a
        # spurious "too large" LayoutError, even in a fresh empty frame). The
        # content is deterministic from self.steps, so rebuilding it per pass
        # still yields identical page breaks between passes.
        def story(page_map):
            return (
                self._cover_elements()
                + self._toc_elements(page_map)
                + [PageBreak()]
                + self._summary_elements()
                + [PageBreak()]
                + self._evidence_elements()
            )

        # --- pass 1: measure which page each step's bookmark lands on ---
        tracker = _TrackingDocTemplate(io.BytesIO(), **doc_kwargs)
        tracker.build(story({}))
        bookmark_pages = tracker.bookmark_pages

        # --- pass 2: render the final PDF with real page numbers ---
        doc = SimpleDocTemplate(path, **doc_kwargs)
        doc.build(
            story(bookmark_pages),
            onFirstPage=self._cover_drawer(),
            onLaterPages=self._page_drawer(),
        )
        return path

    def _build_styles(self, styles) -> dict:
        normal = styles["Normal"]
        return {
            "toc_title": ParagraphStyle(
                "TocTitle", parent=normal, fontName="Helvetica", fontSize=20,
                leading=24, textColor=BRAND, spaceAfter=2,
            ),
            "section": ParagraphStyle(
                "Section", parent=normal, fontName="Helvetica", fontSize=13,
                leading=17, textColor=GREY,
            ),
            "toc": ParagraphStyle("Toc", parent=normal, fontSize=11, leading=14),
            "scenario": ParagraphStyle(
                "Scenario", parent=normal, fontName="Helvetica", fontSize=15,
                leading=20, textColor=INK,
            ),
            "meta": ParagraphStyle("Meta", parent=normal, fontSize=9.5, leading=13),
            "step_title": ParagraphStyle(
                "StepTitle", parent=normal, fontName="Helvetica", fontSize=11,
                leading=15, textColor=INK, spaceBefore=2,
            ),
            "desc": ParagraphStyle("Desc", parent=normal, fontSize=9.5, leading=13),
            "fail_head": ParagraphStyle(
                "FailHead", parent=normal, fontName="Helvetica-Bold", fontSize=10,
                leading=13, textColor=FAIL_COLOR,
            ),
            "fail_body": ParagraphStyle("FailBody", parent=normal, fontSize=9, leading=12),
            "table_head": ParagraphStyle(
                "TableHead", parent=normal, fontSize=10, leading=13, textColor=INK,
            ),
            "table_head_center": ParagraphStyle(
                "TableHeadCenter", parent=normal, fontSize=10, leading=13,
                textColor=INK, alignment=1,
            ),
            "cell_center": ParagraphStyle(
                "CellCenter", parent=normal, fontSize=9, leading=12, alignment=1,
            ),
            "cell": ParagraphStyle("Cell", parent=normal, fontSize=9, leading=12),
            "cell_bold": ParagraphStyle(
                "CellBold", parent=normal, fontName="Helvetica-Bold", fontSize=9,
                leading=12,
            ),
        }

    # ---- cover page ----
    def _cover_elements(self) -> list:
        """The cover is painted on the canvas (see _draw_cover) so the purple
        can run edge to edge; the story only has to claim the page."""
        return [Spacer(1, 1), PageBreak()]

    def _cover_drawer(self):
        def _draw(canv, _doc):
            self._draw_cover(canv)
        return _draw

    def _draw_cover(self, canv):
        page_w, page_h = A4
        canv.saveState()
        canv.setFillColor(BRAND)
        canv.rect(0, 0, page_w, page_h, stroke=0, fill=1)

        if os.path.exists(LOGO_WHITE):
            width = 48 * mm
            height = width * _LOGO_RATIO
            canv.drawImage(LOGO_WHITE, page_w - MARGIN - width,
                           _y(MARGIN + height), width=width, height=height,
                           mask="auto")

        canv.setFillColor(colors.white)
        canv.setFont("Helvetica", 15)
        canv.drawString(MARGIN, _y(24 * mm), COMPANY)
        canv.setFont("Helvetica", 10)
        canv.drawString(MARGIN, _y(31 * mm), DEPARTMENT)

        canv.setFont("Helvetica-Bold", 38)
        canv.drawString(MARGIN, _y(124 * mm), "AUTOMATION")
        canv.drawString(MARGIN, _y(140 * mm), "REPORT")
        canv.setFont("Helvetica", 12)
        canv.drawString(MARGIN, _y(151 * mm), "Testing summary report")

        top = 164 * mm
        canv.setFont("Helvetica", 15)
        for line in self._wrap_cover_text(f"Scenario : {self.scenario()}",
                                          "Helvetica", 15, CONTENT_W):
            canv.drawString(MARGIN, _y(top), line)
            top += 7 * mm

        if self._status == "FAIL" and self.failure_reason():
            top += 2 * mm
            canv.setFont("Helvetica", 10)
            for line in self._wrap_cover_text(f"Failure : {self.failure_reason()}",
                                              "Helvetica", 10, CONTENT_W)[:4]:
                canv.drawString(MARGIN, _y(top), line)
                top += 5 * mm

        right = page_w - MARGIN
        canv.setFont("Helvetica", 11)
        canv.drawRightString(right, _y(225 * mm), "Reporting By")
        canv.setFont("Helvetica", 16)
        canv.drawRightString(right, _y(233 * mm), REPORTING_BY)

        canv.setFont("Helvetica", 11)
        canv.drawString(MARGIN, _y(253 * mm), "Tools :")
        canv.setFont("Helvetica", 16)
        canv.drawString(MARGIN, _y(261 * mm), TOOLS)
        canv.setFont("Helvetica", 10)
        canv.drawRightString(right, _y(261 * mm),
                             self.started_at.strftime("%A %d %B %Y"))
        canv.restoreState()

    @staticmethod
    def _wrap_cover_text(text: str, font: str, size: float, max_width: float) -> list:
        """Greedy word wrap — the cover draws with the canvas, which has no
        paragraph flowing of its own. A single token too wide to fit (a pytest
        node id, say) is broken mid-word rather than left to run off the page."""
        lines, current = [], ""

        def too_wide(candidate: str) -> bool:
            return stringWidth(candidate, font, size) > max_width

        for word in str(text).split():
            candidate = f"{current} {word}".strip()
            if not too_wide(candidate):
                current = candidate
                continue
            if current:
                lines.append(current)
                current = ""
            while too_wide(word):
                cut = len(word)
                while cut > 1 and too_wide(word[:cut]):
                    cut -= 1
                lines.append(word[:cut])
                word = word[cut:]
            current = word
        if current:
            lines.append(current)
        return lines or [""]

    # ---- header / footer on every page after the cover ----
    def _page_drawer(self):
        def _draw(canv, _doc):
            page_w, page_h = A4
            canv.saveState()
            if os.path.exists(LOGO):
                height = 9 * mm
                canv.drawImage(LOGO, MARGIN, _y(12 * mm + height),
                               width=height / _LOGO_RATIO, height=height,
                               mask="auto")
            canv.setFillColor(INK)
            canv.setFont("Helvetica", 13)
            canv.drawString(MARGIN + 54 * mm, _y(15 * mm), COMPANY)
            canv.setFillColor(GREY)
            canv.setFont("Helvetica", 8.5)
            canv.drawString(MARGIN + 54 * mm, _y(20.5 * mm), DEPARTMENT)
            canv.drawString(MARGIN + 54 * mm, _y(25.5 * mm), REPORT_LABEL)
            canv.setFillColor(INK)
            canv.setFont("Helvetica", 9)
            canv.drawRightString(page_w - MARGIN, _y(15 * mm),
                                 self.started_at.strftime("%A %d %B %Y"))
            canv.setStrokeColor(INK)
            canv.setLineWidth(0.6)
            canv.line(MARGIN, _y(HEADER_H - 5 * mm),
                      page_w - MARGIN, _y(HEADER_H - 5 * mm))

            band_y = FOOTER_H - 12 * mm
            canv.setFillColor(BAND)
            canv.rect(MARGIN, band_y, CONTENT_W - 16 * mm, 12 * mm, stroke=0, fill=1)
            canv.rect(page_w - MARGIN - 14 * mm, band_y, 14 * mm, 12 * mm,
                      stroke=0, fill=1)
            canv.setFillColor(GREY)
            canv.setFont("Helvetica", 8)
            canv.drawCentredString(MARGIN + (CONTENT_W - 16 * mm) / 2,
                                   band_y + 4 * mm, FOOTER_TEXT)
            canv.drawCentredString(page_w - MARGIN - 7 * mm, band_y + 4 * mm,
                                   str(canv.getPageNumber()))
            canv.restoreState()
        return _draw

    # ---- table of content ----
    def _toc_elements(self, page_map: dict) -> list:
        s = self._styles
        elements = [
            Paragraph("Table of Content", s["toc_title"]),
            self._brand_rule(),
            Spacer(1, 4 * mm),
        ]
        rows = []
        for index, step in enumerate(self.steps, start=1):
            label = f'{index}. {escape(humanize_step(step["title"]))}'
            if _step_failed(step):
                label += f' <font color="{FAIL_RED_HEX}">- FAILED</font>'
            bookmark = f"step{index}"
            page = page_map.get(bookmark, 1)
            link = f'<a href="#{bookmark}" color="{BRAND_HEX}">'
            rows.append([
                Paragraph(f"{link}{label}</a>", s["toc"]),
                Paragraph(f'{link}{page}</a>', s["toc"]),
            ])
        if rows:
            table = Table(rows, colWidths=[CONTENT_W - 14 * mm, 14 * mm],
                          hAlign="LEFT", rowHeights=9 * mm)
            table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
            ]))
            elements.append(table)
        return elements

    def _brand_rule(self, width: float = 70 * mm):
        """The short purple underline the iOS report puts beneath a heading."""
        rule = Table([[""]], colWidths=[width], rowHeights=[0.1],
                     hAlign="LEFT")
        rule.setStyle(TableStyle([
            ("LINEABOVE", (0, 0), (-1, 0), 0.6, BRAND),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        return rule

    def _section_title(self, text: str) -> list:
        return [
            Paragraph(escape(text), self._styles["section"]),
            self._brand_rule(),
            Spacer(1, 5 * mm),
        ]

    # ---- scenario summary ----
    def _summary_elements(self) -> list:
        s = self._styles
        status = "FAILED" if self._status == "FAIL" else "PASSED"
        duration = (getattr(self, "finished_at", None) or datetime.now()) - self.started_at
        started = self.started_at
        finished = started + duration
        count = len(self.steps)

        elements = [
            Paragraph(f"Scenario : {escape(self.scenario())}", s["scenario"]),
            Spacer(1, 3 * mm),
            self._meta_table([
                ("Total Test Step", f"{count} / {count} Test Step",
                 "Aplication ID", os.getenv("APP_PACKAGE", "app.getswing.dev")),
                ("Scenario Status", status, "Platform Name", self._platform_label()),
                ("Execution Start", started.strftime("%Y-%m-%d %H:%M:%S"),
                 "Host Name", getpass.getuser()),
                ("Execution End", finished.strftime("%Y-%m-%d %H:%M:%S"),
                 "Execution Time", _elapsed(duration.total_seconds())),
            ]),
            Spacer(1, 4 * mm),
        ]
        if status == "FAILED":
            elements += [self._failure_box(), Spacer(1, 3 * mm)]
        elements.append(self._step_table())
        return elements

    def _platform_label(self) -> str:
        device = os.getenv("DEVICE_NAME", "")
        return f"{self.platform} - {device}" if device else str(self.platform)

    def _meta_table(self, rows: list) -> Table:
        s = self._styles["meta"]
        half = CONTENT_W / 2
        body = []
        for left_label, left_value, right_label, right_value in rows:
            body.append([
                Paragraph(escape(left_label), s), Paragraph(":", s),
                Paragraph(escape(str(left_value)), s),
                Paragraph(escape(right_label), s), Paragraph(":", s),
                Paragraph(escape(str(right_value)), s),
            ])
        table = Table(
            body,
            colWidths=[34 * mm, 4 * mm, half - 38 * mm,
                       32 * mm, 4 * mm, half - 36 * mm],
            hAlign="LEFT",
        )
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]))
        return table

    def failure_reason(self) -> str:
        """What went wrong: the error pytest reported, else the last failed
        step's own description."""
        if self.error:
            return self.error.strip().splitlines()[0]
        failed = next((s for s in reversed(self.steps) if _step_failed(s)), None)
        if failed and failed.get("description"):
            return failed["description"]
        return "No failure message was captured for this run"

    def _failure_box(self) -> Table:
        s = self._styles
        rows = [[Paragraph("FAILURE REASON", s["fail_head"])]]
        failed = next(((i, st) for i, st in reversed(list(enumerate(self.steps, start=1)))
                       if _step_failed(st)), None)
        if failed:
            index, step = failed
            rows.append([Paragraph(
                f'Failed at step {index}: {escape(humanize_step(step["title"]))}',
                s["fail_body"])])
        rows.append([Paragraph(escape(self.failure_reason()), s["fail_body"])])
        table = Table(rows, colWidths=[CONTENT_W], hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), FAIL_WASH),
            ("BOX", (0, 0), (-1, -1), 0.6, FAIL_COLOR),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        return table

    def _step_table(self) -> Table:
        s = self._styles
        head, head_center = s["table_head"], s["table_head_center"]
        rows = [[Paragraph("No", head_center), Paragraph("Test Step", head),
                 Paragraph("Status", head_center)]]
        for index, step in enumerate(self.steps, start=1):
            status = _step_status(step)
            color = FAIL_RED_HEX if status == "FAILED" else PASS_GREEN_HEX
            rows.append([
                Paragraph(str(index), s["cell_center"]),
                Paragraph(escape(humanize_step(step["title"])), s["cell"]),
                Paragraph(f'<font color="{color}">{status}</font>', s["cell_center"]),
            ])
        table = Table(rows, colWidths=[16 * mm, CONTENT_W - 46 * mm, 30 * mm],
                      hAlign="LEFT", repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BRAND_TINT),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ]))
        return table

    # ---- evidence ----
    def _evidence_elements(self) -> list:
        s = self._styles
        elements = self._section_title("TEST CASE EVIDENCE IMAGE")
        for index, step in enumerate(self.steps, start=1):
            label = humanize_step(step["title"])
            body, caption = self._step_body(step)
            shot = step["screenshot"]
            image = (self._fit_image(
                shot, max_height=TABLE_IMAGE_H if body is not None else IMAGE_MAX_H
            ) if shot and os.path.exists(shot) else None)

            # keep the heading with its screenshot instead of stranding it at
            # the foot of the previous page
            needed = 14 * mm + (image.drawHeight if image is not None else 0)
            elements.append(CondPageBreak(min(needed, CONTENT_H)))

            # <a name> makes this the TOC link's click target; the custom
            # _toc_bookmark attribute is how the measurement pass finds it.
            title_para = Paragraph(
                f'<a name="step{index}"/>{index}. {escape(label)}', s["step_title"]
            )
            title_para._toc_bookmark = f"step{index}"
            elements.append(title_para)

            if image is not None:
                elements.append(Spacer(1, 2 * mm))
                elements.append(image)

            status = _step_status(step)
            color = FAIL_RED_HEX if status == "FAILED" else PASS_GREEN_HEX
            elements.append(Spacer(1, 2 * mm))
            elements.append(Paragraph(
                f'Desc : <font color="{color}">[{status}]</font> '
                f'{escape(caption or label)}',
                s["desc"],
            ))
            if body is not None:
                elements.append(Spacer(1, 1.5 * mm))
                elements.append(body)
            elements.append(Spacer(1, 6 * mm))
        return elements

    def _step_body(self, step: dict):
        """How a step's detail renders: (table, caption). A compare or data
        dict becomes a table under the caption; a 'k=v | k=v' description
        becomes the table itself, so it isn't printed twice."""
        description = step.get("description") or ""
        if step.get("compare"):
            return self._compare_table(step["compare"]), description
        if step.get("data"):
            return self._kv_table(step["data"]), description
        parsed = _parse_kv(description)
        if parsed:
            return self._kv_table(parsed), ""
        return None, description

    def _p(self, text, bold=False):
        style = self._cell_bold if bold else self._cell_style
        text = "—" if text in (None, "") else str(text)
        return Paragraph(escape(text), style)

    def _kv_table(self, data: dict) -> Table:
        """A 'list-down' Field/Value table."""
        rows = [[self._p("Field", bold=True), self._p("Value", bold=True)]]
        rows += [[self._p(k, bold=True), self._p(v)] for k, v in data.items()]
        table = Table(rows, colWidths=[5 * cm, CONTENT_W - 5 * cm], hAlign="LEFT")
        table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, LINE),
            ("BACKGROUND", (0, 0), (-1, 0), BRAND_TINT),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        return table

    def _compare_table(self, compare: dict) -> Table:
        """A side-by-side Field | left | right table; mismatches in red."""
        before = compare.get("before") or {}
        after = compare.get("after") or {}
        left_label = compare.get("left_label", "Before")
        right_label = compare.get("right_label", "After")
        mismatches = set(compare.get("mismatch_fields") or [])
        fields = list(before.keys()) + [k for k in after if k not in before]

        rows = [[self._p("Field", bold=True), self._p(left_label, bold=True),
                 self._p(right_label, bold=True)]]
        for f in fields:
            rows.append([self._p(f, bold=True), self._p(before.get(f, "")),
                         self._p(after.get(f, ""))])

        half = (CONTENT_W - 4 * cm) / 2
        table = Table(rows, colWidths=[4 * cm, half, half], hAlign="LEFT")
        style = [
            ("GRID", (0, 0), (-1, -1), 0.4, LINE),
            ("BACKGROUND", (0, 0), (-1, 0), BRAND_TINT),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]
        for idx, f in enumerate(fields, start=1):
            row_color = FAIL_COLOR if f in mismatches else PASS_COLOR
            style.append(("TEXTCOLOR", (1, idx), (2, idx), row_color))
            if f in mismatches:
                style.append(("BACKGROUND", (0, idx), (-1, idx), FAIL_WASH))
        table.setStyle(TableStyle(style))
        return table

    @staticmethod
    def _fit_image(path: str, max_width: float = IMAGE_MAX_W,
                   max_height: float = IMAGE_MAX_H):
        """Scale a screenshot to fit the page while keeping aspect ratio."""
        from reportlab.lib.utils import ImageReader

        iw, ih = ImageReader(path).getSize()
        ratio = min(max_width / iw, max_height / ih)
        image = Image(path, width=iw * ratio, height=ih * ratio)
        image.hAlign = "CENTER"
        return image


# --------------------------------------------------------------------------- #
# Callable helpers — use these in a test to run WITH or WITHOUT a PDF.
#
# The intended shape of a test is:
#
#     def test_something(self, login_flow):
#         pdf = init_pdf("test_something")   # first line
#         login_flow.open_login()            # ... steps ...
#         generate_pdf(pdf)                  # after the last step
#
# ``init_pdf`` attaches the reporter to every flow the test asked for as a
# fixture, so the test never wires it by hand: the flow fixtures in conftest.py
# register their flows here (``register_flow``) while they are being built,
# which happens before the test body runs.
# --------------------------------------------------------------------------- #

# Flows built for the CURRENT test, waiting for a reporter. Cleared per test by
# the pdf_evidence fixture in conftest.py.
_registered_flows: list = []

# The reporter the current test opened, and whether it has been written out —
# lets conftest write a FAIL report for a test that blew up before reaching its
# own generate_pdf() line.
_active: dict = {}


def register_flow(flow):
    """Remember a flow so the test's ``init_pdf()`` can attach the reporter to
    it. Returns the flow, so a fixture reads ``return register_flow(Flow(...))``."""
    _registered_flows.append(flow)
    return flow


def reset_evidence():
    """Forget the previous test's flows and reporter. Called once per test."""
    _registered_flows.clear()
    _active.clear()


def active_reporter() -> "PDFReporter | None":
    """The reporter opened by the current test (None when there is none, or
    when PDF evidence is off)."""
    return _active.get("reporter")


def evidence_written() -> bool:
    """True once ``generate_pdf`` has run for the current test's reporter."""
    return bool(_active.get("generated"))


def active_pdf_path() -> str | None:
    """Path of the PDF written for the current test, if one was written."""
    return _active.get("path")


def init_pdf(test_name: str, enabled: bool | None = None,
             tc_id: str | None = None, tc_name: str | None = None) -> "PDFReporter | None":
    if enabled is None:
        enabled = settings.PDF_EVIDENCE
    reporter = (
        PDFReporter(test_name, settings.PLATFORM, tc_id=tc_id, tc_name=tc_name)
        if enabled else None
    )
    for flow in _registered_flows:
        flow.use_reporter(reporter)
    _active.update(reporter=reporter, path=None, generated=False)
    return reporter


def generate_pdf(reporter: "PDFReporter | None", status: str = "PASS",
                 error: str = "") -> str | None:
    if _active.get("reporter") is reporter:
        _active["generated"] = True
    if reporter is None:
        return None
    path = reporter.generate(status=status, error=error)
    if _active.get("reporter") is reporter:
        _active["path"] = path
    print(f"\n[evidence] PDF written to: {path}")
    return path
