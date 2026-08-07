"""
Android XPaths for the Swing Tee Time > Booking details screen.

Opened from "See booking details" on the confirmed screen (also reachable from
Activity/History). Flutter app — values surface through ``content-desc``. This
screen mixes two layouts:
  * Booking summary  -> label and value are SEPARATE sibling ``View`` nodes
                        (value read via the label's following-sibling).
  * Payment summary  -> a row is one combined "Label\\nvalue" node (parsed in the
                        page object). "Total payment" is an ``ImageView``.
"""


class BookingDetailsLocators:
    # --- header ---
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Booking details" and @heading="true"]'

    # --- booking summary ---
    label_booking_summary = '//android.view.View[@content-desc="Booking summary"]'
    # status badge: UPCOMING / ONGOING / COMPLETED / CANCELLED
    label_status = ('//android.view.View[@content-desc="UPCOMING" or @content-desc="ONGOING"'
                    ' or @content-desc="COMPLETED" or @content-desc="CANCELLED"]')
    label_booking_id = '//android.view.View[starts-with(@content-desc,"Booking #")]'

    # summary rows: value = the View right after the label View
    value_date = '//android.view.View[@content-desc="Date"]/following-sibling::android.view.View[1]'
    value_session = '//android.view.View[@content-desc="Session"]/following-sibling::android.view.View[1]'
    value_preferred_time = '//android.view.View[@content-desc="Preferred time"]/following-sibling::android.view.View[1]'
    value_no_of_players = '//android.view.View[@content-desc="No. of players"]/following-sibling::android.view.View[1]'
    button_see_complete_breakdown = '//android.widget.Button[@content-desc="See complete breakdown"]'

    # --- payment summary (combined "Label\nvalue" nodes) ---
    label_payment_summary = '//android.view.View[@content-desc="Payment summary"]'
    row_subtotal = '//android.view.View[starts-with(@content-desc,"Subtotal")]'
    row_processing_fee = '//android.view.View[starts-with(@content-desc,"Processing fee")]'
    # "Total payment" is an ImageView on this screen -> match any node.
    row_total_payment = '//*[starts-with(@content-desc,"Total payment")]'

    # swing credits earned (separate label + value)
    label_credits_earned = '//android.view.View[@content-desc="Swing Credits you earned"]'
    value_credits_earned = '//android.view.View[@content-desc="Swing Credits you earned"]/following-sibling::android.view.View[1]'
    label_credits_note = '//android.view.View[contains(@content-desc,"Swing Credits will only be issued")]'

    # --- actions / history ---
    button_see_receipt = '//android.widget.Button[@content-desc="See receipt"]'
    label_history = '//android.view.View[@content-desc="History"]'
    # timeline entry, e.g. "Booking confirmed\n16:50, 6 Aug 2026"
    timeline_booking_confirmed = '//android.widget.ImageView[starts-with(@content-desc,"Booking confirmed")]'
