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
  * Page 1  -> cover: full-bleed Swing purple with the white logo, the report
               title, TC ID / TC Name and the run's meta (platform, date,
               status pill, step count). Drawn straight on the canvas.
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

# --- brand ---------------------------------------------------------------- #
# Sampled from the app's own launcher icon (assets/swing_rounded_android.png):
# rgb(92, 0, 230). The tints are that hue lightened for rules and muted labels.
BRAND_PURPLE = colors.HexColor("#5C00E6")
BRAND_PURPLE_DARK = colors.HexColor("#3D0099")
BRAND_TINT = colors.HexColor("#C9A9FF")      # labels on the purple cover
BRAND_WASH = colors.HexColor("#F3EBFF")      # table header fill on white pages

_ASSETS_DIR = os.path.join(settings.BASE_DIR, "assets")
# The launcher icon: white wordmark on exactly BRAND_PURPLE, so dropping it on
# the purple cover reads as the logo floating on the page.
LOGO_ON_PURPLE = os.path.join(_ASSETS_DIR, "swing_rounded_android.png")
# Purple wordmark on transparency — for anything on a white background.
LOGO_ON_WHITE = os.path.join(_ASSETS_DIR, "swing_logo_horizontal.png")


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
        tracker.build(self._cover_elements() + placeholder_toc + [PageBreak()] + self._step_elements())
        bookmark_pages = tracker.bookmark_pages
        total_pages = tracker.last_content_page

        # --- pass 2: render the final PDF with a real dotted-leader TOC ---
        real_toc = self._toc_elements(bookmark_pages, content_width, placeholder=False)
        elements = self._cover_elements() + real_toc + [PageBreak()] + self._step_elements()

        doc = SimpleDocTemplate(path, **doc_kwargs)
        doc.build(
            elements,
            onFirstPage=lambda canv, _doc: self._draw_cover(canv, status),
            onLaterPages=self._footer_drawer(total_pages),
        )
        return path

    def _build_styles(self, styles) -> dict:
        return {
            "toc_title": ParagraphStyle(
                "TocTitle", parent=styles["Heading2"], spaceBefore=6, spaceAfter=6,
                textColor=BRAND_PURPLE,
            ),
            "toc": ParagraphStyle("Toc", parent=styles["Normal"], fontSize=10, leading=18),
            "step_title": ParagraphStyle(
                "StepTitle", parent=styles["Heading3"], spaceBefore=10, spaceAfter=2,
                textColor=BRAND_PURPLE_DARK,
            ),
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
    def _cover_elements(self) -> list:
        """The cover is painted on the canvas (see _draw_cover) so the purple
        can run edge to edge; the story only has to claim the page."""
        return [Spacer(1, 1), PageBreak()]

    def _draw_cover(self, canv, status: str):
        page_w, page_h = A4
        canv.saveState()

        # full-bleed brand purple
        canv.setFillColor(BRAND_PURPLE)
        canv.rect(0, 0, page_w, page_h, stroke=0, fill=1)

        # the launcher icon sits on the same purple, so what shows is the mark
        top = page_h - 4.2 * cm
        if os.path.exists(LOGO_ON_PURPLE):
            size = 4.6 * cm
            canv.drawImage(LOGO_ON_PURPLE, 2.2 * cm, top - size + 1.1 * cm,
                           width=size, height=size, mask="auto")
            top -= size - 0.6 * cm
        else:  # asset missing — fall back to the wordmark as type
            canv.setFillColor(colors.white)
            canv.setFont("Helvetica-Bold", 34)
            canv.drawString(2.2 * cm, top, "swing")
            top -= 1.4 * cm

        # title
        canv.setFillColor(colors.white)
        canv.setFont("Helvetica-Bold", 30)
        canv.drawString(2.2 * cm, top, "Test Evidence Report")

        canv.setFillColor(BRAND_TINT)
        canv.setFont("Helvetica", 11)
        canv.drawString(2.2 * cm, top - 0.85 * cm, _CONFIDENTIAL_NOTICE.upper())

        # thin rule under the header
        canv.setStrokeColor(BRAND_TINT)
        canv.setLineWidth(0.7)
        canv.line(2.2 * cm, top - 1.6 * cm, page_w - 2.2 * cm, top - 1.6 * cm)

        # test case, big and unmissable
        y = top - 3.0 * cm
        if self.tc_id:
            canv.setFillColor(colors.white)
            canv.setFont("Helvetica-Bold", 20)
            canv.drawString(2.2 * cm, y, self.tc_id)
            y -= 1.0 * cm
        if self.tc_name:
            canv.setFillColor(colors.white)
            canv.setFont("Helvetica", 14)
            for line in self._wrap_cover_text(self.tc_name, "Helvetica", 14,
                                              page_w - 4.4 * cm):
                canv.drawString(2.2 * cm, y, line)
                y -= 0.7 * cm

        # result, right under the case it belongs to
        self._draw_status_pill(canv, 2.2 * cm, y - 0.5 * cm, status)

        # meta block, anchored to the foot of the page so the cover reads as
        # header at the top / details at the bottom instead of drifting
        inner = page_w - 4.4 * cm
        y = 7.4 * cm
        canv.setStrokeColor(BRAND_PURPLE_DARK)
        canv.setLineWidth(0.7)
        canv.line(2.2 * cm, y + 1.0 * cm, page_w - 2.2 * cm, y + 1.0 * cm)

        # the pytest node id gets a full-width row of its own; the short fields
        # share the row below it
        self._draw_meta_field(canv, 2.2 * cm, y, "TEST", self.test_name, inner)
        y -= 2.0 * cm
        for index, (label, value) in enumerate((
            ("PLATFORM", self.platform),
            ("DATE", self.started_at.strftime("%Y-%m-%d %H:%M:%S")),
            ("STEPS", str(len(self.steps))),
        )):
            column = inner / 3
            self._draw_meta_field(canv, 2.2 * cm + index * column, y, label, value,
                                  column - 0.6 * cm)

        # footer band
        canv.setFillColor(BRAND_PURPLE_DARK)
        canv.rect(0, 0, page_w, 1.6 * cm, stroke=0, fill=1)
        canv.setFillColor(BRAND_TINT)
        canv.setFont("Helvetica", 8)
        canv.drawString(2.2 * cm, 0.62 * cm, _CONFIDENTIAL_NOTICE)
        canv.drawRightString(page_w - 2.2 * cm, 0.62 * cm, "Page 1")
        canv.restoreState()

    @classmethod
    def _draw_meta_field(cls, canv, x: float, y: float, label: str, value, width: float):
        """One 'LABEL / value' pair of the cover's meta block."""
        canv.setFillColor(BRAND_TINT)
        canv.setFont("Helvetica", 8)
        canv.drawString(x, y, label)
        canv.setFillColor(colors.white)
        canv.setFont("Helvetica", 11)
        for line_no, line in enumerate(
            cls._wrap_cover_text(str(value), "Helvetica", 11, width)[:2]
        ):
            canv.drawString(x, y - 0.55 * cm - line_no * 0.5 * cm, line)

    @staticmethod
    def _draw_status_pill(canv, x: float, y: float, status: str):
        """PASS / FAIL as a rounded pill — the one thing a reader looks for."""
        label = (status or "N/A").upper()
        fill = {"PASS": colors.HexColor("#0FA958"), "FAIL": colors.HexColor("#E5484D")}.get(
            label, colors.HexColor("#6B7280")
        )
        text_w = stringWidth(label, "Helvetica-Bold", 12)
        width, height = text_w + 1.6 * cm, 0.95 * cm
        canv.setFillColor(fill)
        canv.roundRect(x, y - height, width, height, height / 2, stroke=0, fill=1)
        canv.setFillColor(colors.white)
        canv.setFont("Helvetica-Bold", 12)
        canv.drawCentredString(x + width / 2, y - height + 0.31 * cm, label)

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
        return f'<a href="#{bookmark}" color="#5C00E6">{label} {dots} {page_str}</a>'

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

    def _footer_drawer(self, total_pages: int):
        """Returns an onLaterPages callback: a purple hairline, the Swing
        wordmark, the confidentiality line and "Page X of Y"."""
        def _draw(canv, doc):
            canv.saveState()
            page_w, _ = A4
            canv.setStrokeColor(BRAND_PURPLE)
            canv.setLineWidth(0.7)
            canv.line(1.5 * cm, 1.45 * cm, page_w - 1.5 * cm, 1.45 * cm)
            if os.path.exists(LOGO_ON_WHITE):
                width = 1.9 * cm
                canv.drawImage(LOGO_ON_WHITE, 1.5 * cm, 0.85 * cm, width=width,
                               height=width * 64 / 214, mask="auto")
            canv.setFont("Helvetica", 8)
            canv.setFillColor(colors.grey)
            canv.drawCentredString(page_w / 2, 1.0 * cm, _CONFIDENTIAL_NOTICE)
            canv.setFillColor(BRAND_PURPLE)
            canv.drawRightString(page_w - 1.5 * cm, 1.0 * cm,
                                 f"Page {canv.getPageNumber()} of {total_pages}")
            canv.restoreState()
        return _draw

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
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DCCBFF")),
            ("BACKGROUND", (0, 0), (-1, 0), BRAND_WASH),
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
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DCCBFF")),
            ("BACKGROUND", (0, 0), (-1, 0), BRAND_WASH),
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


def generate_pdf(reporter: "PDFReporter | None", status: str = "PASS") -> str | None:
    """
    Build the PDF from a reporter — call it after the test's last step. No-op
    (returns None) when reporter is None, so the same call works whether or not
    evidence was enabled.

    The file always lands in reports/. A run that reports to ClickUp uploads it
    from there and then removes it — see utils/clickup_reporter.py and
    settings.PDF_CLEANUP.
    """
    if _active.get("reporter") is reporter:
        _active["generated"] = True
    if reporter is None:
        return None
    path = reporter.generate(status=status)
    if _active.get("reporter") is reporter:
        _active["path"] = path
    print(f"\n[evidence] PDF written to: {path}")
    return path
