"""
Android XPaths for the Swing Driving Range > Cancellation details screen.

Opened from the Booking cancelled screen ('See cancellation details') or My
Bookings. Read-only: booking summary, cancellation reason, refund destination
(bank account) and the refund breakdown.

Flutter app — values surface through ``content-desc``. Rows are a label View
next to a value View (read via the label's following sibling).
"""


class CancellationDetailsLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Cancellation details"]'
    button_back = '//android.view.View[@content-desc="Cancellation details"]/preceding-sibling::android.widget.ImageView[1]'

    # ================= summary =================
    label_range_name = '//android.view.View[@content-desc="%s"]'
    # value_by_label % "Booking ID" -> "#GSHRC", % "Cancellation reason" -> "Bad weather", etc.
    value_by_label = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View[1]'

    label_cancellation_reason = '//android.view.View[@content-desc="Cancellation reason"]'

    # ================= refund destination =================
    label_refund_destination = '//android.view.View[@content-desc="Refund destination"]'
    # "Bank name" -> "BPD Bali", "Account number" -> "12354", "Account holder name" -> "SRRR"

    # ================= refund details =================
    label_refund_details = '//android.view.View[@content-desc="Refund details"]'
    value_original_total = '//android.view.View[@content-desc="Original total paid"]/following-sibling::android.view.View[1]'
    # "Total refund (50%)" -> "Rp. 1,500,000" (percent varies)
    label_total_refund = '//android.view.View[starts-with(@content-desc,"Total refund")]'
    value_total_refund = '//android.view.View[starts-with(@content-desc,"Total refund")]/following-sibling::android.view.View[1]'
    label_refund_process = '//*[contains(@content-desc,"business days")]'
