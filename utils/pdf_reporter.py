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

Layout:
  * Page 1  -> cover: Swing brand + confidentiality notice, TC ID / TC Name,
               and the run's meta table (test/platform/date/status/steps).
  * Page 2+ -> Table of contents: one dotted-leader line per step
               ("Label ....... 3"), the whole line clickable, jumping straight
               to that step's page — real page numbers, computed with a first
               "measurement" pass over the same content (afterFlowable hook)
               before the final PDF is rendered.
  * Every page carries a footer: "Swing — Confidential. For Swing use only."
               plus "Page X of Y".

When PDF evidence is disabled no reporter is created, page objects receive
``None``, and nothing here runs — the automation runs exactly the same, just
without a PDF.
"""
import io
import os
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    SimpleDocTemplate,
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

# Brand line shown on the cover and in every page's footer.
_CONFIDENTIAL_NOTICE = "Swing — Confidential. For Swing use only."


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
    can render a Table of contents with accurate page numbers — the standard
    two-pass technique reportlab's own TableOfContents/multiBuild uses
    internally, done by hand here so we control the dotted-leader layout."""

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
                 data: dict | None = None, compare: dict | None = None):
        self.steps.append(
            {
                "title": title,
                "description": description,
                "screenshot": screenshot,
                "data": data,
                "compare": compare,
                "time": datetime.now(),
            }
        )

    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def generate(self, status: str = "", output_dir: str | None = None) -> str:
        """Render the collected steps into a PDF and return its file path."""
        output_dir = output_dir or settings.REPORTS_DIR
        os.makedirs(output_dir, exist_ok=True)

        stamp = self.started_at.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.test_name}_{self.platform}_{stamp}.pdf"
        path = os.path.join(output_dir, filename)

        doc_kwargs = dict(
            pagesize=A4,
            topMargin=1.5 * cm, bottomMargin=1.5 * cm,
            leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        )
        content_width = A4[0] - doc_kwargs["leftMargin"] - doc_kwargs["rightMargin"]

        styles = getSampleStyleSheet()
        self._styles = self._build_styles(styles)
        self._cell_style = self._styles["cell"]
        self._cell_bold = self._styles["cell_bold"]

        # NOTE: flowables must be freshly built for EACH pass — reportlab
        # Image/Paragraph flowables are not safe to reuse across two separate
        # doc.build() calls (confirmed empirically: reusing the same objects
        # makes the second build misjudge available frame space and raise a
        # spurious "too large" LayoutError, even in a fresh empty frame). The
        # content is deterministic from self.steps, so rebuilding it per pass
        # still yields identical page breaks between passes.

        # --- pass 1: measure which page each step's bookmark lands on ---
        tracker = _TrackingDocTemplate(io.BytesIO(), **doc_kwargs)
        placeholder_toc = self._toc_elements({}, content_width, placeholder=True)
        tracker.build(self._cover_elements(status) + placeholder_toc + [PageBreak()] + self._step_elements())
        bookmark_pages = tracker.bookmark_pages
        total_pages = tracker.last_content_page

        # --- pass 2: render the final PDF with a real dotted-leader TOC ---
        real_toc = self._toc_elements(bookmark_pages, content_width, placeholder=False)
        elements = self._cover_elements(status) + real_toc + [PageBreak()] + self._step_elements()

        doc = SimpleDocTemplate(path, **doc_kwargs)
        footer = self._footer_drawer(total_pages)
        doc.build(elements, onFirstPage=footer, onLaterPages=footer)
        return path

    def _build_styles(self, styles) -> dict:
        return {
            "brand": ParagraphStyle(
                "Brand", parent=styles["Title"], fontSize=28,
                textColor=colors.HexColor("#0f6b52"), spaceAfter=2,
            ),
            "confidential": ParagraphStyle(
                "Confidential", parent=styles["Normal"], fontSize=9,
                textColor=colors.HexColor("#b00020"), spaceAfter=16,
            ),
            "title": ParagraphStyle("TitleBig", parent=styles["Title"], fontSize=18, spaceAfter=10),
            "tc": ParagraphStyle("TcId", parent=styles["Heading2"], fontSize=13, spaceAfter=4),
            "toc_title": ParagraphStyle("TocTitle", parent=styles["Heading2"], spaceBefore=6, spaceAfter=6),
            "toc": ParagraphStyle("Toc", parent=styles["Normal"], fontSize=10, leading=18),
            "step_title": ParagraphStyle("StepTitle", parent=styles["Heading3"], spaceBefore=10, spaceAfter=2),
            "caption": ParagraphStyle(
                "Caption", parent=styles["Normal"], fontSize=9, textColor=colors.grey,
                alignment=0, spaceBefore=2,
            ),
            "cell": ParagraphStyle("Cell", parent=styles["Normal"], fontSize=9, leading=12),
            "cell_bold": ParagraphStyle(
                "CellBold", parent=ParagraphStyle("Cell", parent=styles["Normal"], fontSize=9, leading=12),
                fontName="Helvetica-Bold",
            ),
        }

    # ---- cover page ----
    def _cover_elements(self, status: str) -> list:
        s = self._styles
        elements = [
            Paragraph("Swing", s["brand"]),
            Paragraph(_CONFIDENTIAL_NOTICE.upper(), s["confidential"]),
            Paragraph("Test Evidence Report", s["title"]),
        ]
        if self.tc_id or self.tc_name:
            elements.append(Paragraph(f"TC ID: {escape(self.tc_id or '—')}", s["tc"]))
            elements.append(Paragraph(f"TC Name: {escape(self.tc_name or '—')}", s["tc"]))
            elements.append(Spacer(1, 0.3 * cm))
        elements.append(self._meta_table(status))
        elements.append(PageBreak())
        return elements

    # ---- table of contents ----
    # Reserve room for the frame's own internal padding (reportlab subtracts a
    # further ~6pt each side beyond the doc margins) so a line filled right up
    # to content_width doesn't clip/wrap.
    _TOC_FRAME_PADDING = 14

    def _toc_elements(self, page_map: dict, content_width: float, placeholder: bool) -> list:
        s = self._styles
        elements = [Paragraph("Table of contents", s["toc_title"])]
        for i, step in enumerate(self.steps, start=1):
            label = f'{i}. {escape(humanize_step(step["title"]))}'
            when = step["time"].strftime("%H:%M:%S")
            when_suffix = f"   ({when})"
            when_w = stringWidth(when_suffix, "Helvetica", 8)
            bookmark = f"step{i}"
            page_str = "1" if placeholder else str(page_map.get(bookmark, 1))
            # dots must leave room for the trailing timestamp suffix appended
            # after them, or the whole line overflows and wraps onto a second
            # line instead of sitting flush with the label.
            available = content_width - when_w - self._TOC_FRAME_PADDING
            line = self._dotted_toc_line(label, page_str, bookmark, s["toc"], available)
            elements.append(Paragraph(
                f'{line}<font color="grey" size="8">{when_suffix}</font>',
                s["toc"],
            ))
        return elements

    @staticmethod
    def _dotted_toc_line(label: str, page_str: str, bookmark: str,
                         style: ParagraphStyle, available_width: float) -> str:
        """'<label> ....... <page>', dot count computed from real font metrics
        so the leader fills the line regardless of label/page-number length,
        the whole thing wrapped as one clickable link to that step."""
        font_name, font_size = style.fontName, style.fontSize
        label_w = stringWidth(label + " ", font_name, font_size)
        page_w = stringWidth(" " + page_str, font_name, font_size)
        dot_w = stringWidth(".", font_name, font_size) or 1
        remaining = available_width - label_w - page_w
        n_dots = max(3, int(remaining / dot_w))
        dots = "." * n_dots
        return f'<a href="#{bookmark}" color="blue">{label} {dots} {page_str}</a>'

    # ---- steps ----
    def _step_elements(self) -> list:
        s = self._styles
        elements = []
        for i, step in enumerate(self.steps, start=1):
            title = escape(humanize_step(step["title"]))
            when = step["time"].strftime("%H:%M:%S")
            # <a name> makes this the TOC link's click target; the custom
            # _toc_bookmark attribute is how the measurement pass finds it.
            title_para = Paragraph(
                f'<a name="step{i}"/>Step {i}: {title}  '
                f'<font color="grey" size="9">({when})</font>',
                s["step_title"],
            )
            title_para._toc_bookmark = f"step{i}"
            elements.append(title_para)

            shot = step["screenshot"]
            if shot and os.path.exists(shot):
                elements.append(Spacer(1, 0.2 * cm))
                elements.append(self._fit_image(shot))

            body = self._step_body(step, s["caption"])
            if body is not None:
                elements.append(Spacer(1, 0.15 * cm))
                elements.append(body)
            elements.append(Spacer(1, 0.4 * cm))
        return elements

    @staticmethod
    def _footer_drawer(total_pages: int):
        """Returns an onFirstPage/onLaterPages callback drawing the
        confidentiality footer + "Page X of Y" on every page."""
        def _draw(canv, doc):
            canv.saveState()
            canv.setFont("Helvetica", 8)
            canv.setFillColor(colors.grey)
            page_w, _ = A4
            canv.drawCentredString(page_w / 2, 1.0 * cm, _CONFIDENTIAL_NOTICE)
            canv.drawRightString(page_w - 1.5 * cm, 1.0 * cm,
                                 f"Page {canv.getPageNumber()} of {total_pages}")
            canv.restoreState()
        return _draw

    def _meta_table(self, status: str) -> Table:
        status_color = colors.green if status.upper() == "PASS" else (
            colors.red if status.upper() == "FAIL" else colors.grey
        )
        meta = Table(
            [
                ["Test", self.test_name],
                ["Platform", self.platform],
                ["Date", self.started_at.strftime("%Y-%m-%d %H:%M:%S")],
                ["Status", status or "N/A"],
                ["Steps", str(len(self.steps))],
            ],
            colWidths=[3 * cm, 12 * cm],
        )
        meta.setStyle(TableStyle([
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.grey),
            ("TEXTCOLOR", (1, 3), (1, 3), status_color),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.lightgrey),
        ]))
        return meta

    def _step_body(self, step: dict, caption_style):
        """Pick how a step's data renders: compare table > data table >
        parsed key=value table > plain caption."""
        if step.get("compare"):
            return self._compare_table(step["compare"])
        data = step.get("data") or _parse_kv(step.get("description", ""))
        if data:
            return self._kv_table(data)
        if step.get("description"):
            return Paragraph(escape(step["description"]), caption_style)
        return None

    def _p(self, text, bold=False):
        style = self._cell_bold if bold else self._cell_style
        text = "—" if text in (None, "") else str(text)
        return Paragraph(escape(text), style)

    def _kv_table(self, data: dict) -> Table:
        """A 'list-down' Field/Value table."""
        rows = [[self._p("Field", bold=True), self._p("Value", bold=True)]]
        rows += [[self._p(k, bold=True), self._p(v)] for k, v in data.items()]
        table = Table(rows, colWidths=[5 * cm, 12.5 * cm], hAlign="LEFT")
        table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
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

        rows = [[self._p("Field", bold=True), self._p(left_label, bold=True), self._p(right_label, bold=True)]]
        for f in fields:
            rows.append([self._p(f, bold=True), self._p(before.get(f, "")), self._p(after.get(f, ""))])

        table = Table(rows, colWidths=[4 * cm, 6.75 * cm, 6.75 * cm], hAlign="LEFT")
        style = [
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]
        for idx, f in enumerate(fields, start=1):
            row_color = colors.HexColor("#b00020") if f in mismatches else colors.HexColor("#1b5e20")
            style.append(("TEXTCOLOR", (1, idx), (2, idx), row_color))
            if f in mismatches:
                style.append(("BACKGROUND", (0, idx), (-1, idx), colors.HexColor("#fdecea")))
        table.setStyle(TableStyle(style))
        return table

    @staticmethod
    def _fit_image(path: str, max_width: float = 9 * cm, max_height: float = 14 * cm):
        """Scale a screenshot to fit the page while keeping aspect ratio."""
        from reportlab.lib.utils import ImageReader

        iw, ih = ImageReader(path).getSize()
        ratio = min(max_width / iw, max_height / ih)
        return Image(path, width=iw * ratio, height=ih * ratio)


# --------------------------------------------------------------------------- #
# Callable helpers — use these in a test to run WITH or WITHOUT a PDF.
# --------------------------------------------------------------------------- #
def init_pdf(test_name: str, enabled: bool | None = None,
             tc_id: str | None = None, tc_name: str | None = None) -> "PDFReporter | None":
    """
    Create a PDFReporter, or return None when PDF evidence is off.

    ``enabled`` defaults to ``settings.PDF_EVIDENCE`` (env var / --pdf flag), so:
        pdf = init_pdf("test_login")        # None unless evidence is enabled
        pdf = init_pdf("test_login", True)  # force a PDF for this test
    Pass ``tc_id``/``tc_name`` when you already know them (otherwise tc_id is
    guessed from a parametrized test name and can be corrected later via
    ``reporter.set_test_case(...)``). Pass the result into the page objects.
    When it is None, capture_step still screenshots but no PDF is produced.
    """
    if enabled is None:
        enabled = settings.PDF_EVIDENCE
    return PDFReporter(test_name, settings.PLATFORM, tc_id=tc_id, tc_name=tc_name) if enabled else None


def generate_pdf(reporter: "PDFReporter | None", status: str = "PASS") -> str | None:
    """
    Build the PDF from a reporter. No-op (returns None) when reporter is None,
    so the same call works whether or not evidence was enabled.
    """
    if reporter is None:
        return None
    path = reporter.generate(status=status)
    print(f"\n[evidence] PDF written to: {path}")
    return path
