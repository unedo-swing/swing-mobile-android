"""
Android XPaths for the Swing Driving Range > Confirm cancellation screen.

Opened from Change Booking > Cancellation tab > 'Continue cancel'. Shows the
booking summary, a cancellation-reason radio list, a refund destination (bank
account) and a refund breakdown, then a 'Confirm & cancel' action (disabled
until a reason + bank details are provided).

Flutter app — values surface through ``content-desc``; the bank fields expose a
``hint`` instead. Summary rows are a label View next to a value View.
"""


class ConfirmCancellationLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Confirm cancellation"]'
    button_back = '//android.view.View[@content-desc="Confirm cancellation"]/preceding-sibling::android.widget.ImageView[1]'

    # ================= booking summary =================
    label_range_name = '//android.view.View[@content-desc="%s"]'
    # value_by_label % "Booking ID" -> "#GSHRC", % "Cancellation date & time" -> "13:10, 6 Aug 2026"
    value_by_label = '//android.view.View[@content-desc="%s"]/following-sibling::android.view.View[1]'

    # ================= cancellation reason =================
    label_cancellation_reason = '//android.view.View[@content-desc="Cancellation reason"]'
    # a reason radio by name, e.g. "Bad weather", "Wrong driving range booked"
    reason_by_name = '//android.widget.RadioButton[@content-desc="%s"]'

    # ================= refund destination =================
    label_refund_destination = '//android.view.View[@content-desc="Refund destination"]'
    label_add_bank_prompt = '//*[contains(@content-desc,"Add your bank account")]'
    # the "Select Bank" field (opens the Select bank dialog)
    button_select_bank = '//android.view.View[@content-desc="Select Bank"]'
    input_bank_account_number = '//*[@hint="Bank account number"]'
    input_bank_account_name = '//*[@hint="Bank account name"]'

    # ================= refund details =================
    label_refund_details = '//android.view.View[@content-desc="Refund details"]'
    value_original_total = '//android.view.View[@content-desc="Original total paid"]/following-sibling::android.view.View[1]'
    # "Total refunded (50%)" -> "Rp. 1,500,000" (percent varies)
    label_total_refunded = '//android.view.View[starts-with(@content-desc,"Total refunded")]'
    value_total_refunded = '//android.view.View[starts-with(@content-desc,"Total refunded")]/following-sibling::android.view.View[1]'
    label_refund_process = '//*[contains(@content-desc,"business days")]'

    # ================= confirm =================
    # ImageView, enabled=false until a reason + bank details are filled in
    button_confirm_cancel = '//*[@content-desc="Confirm & cancel"]'

    # ================= confirm dialog (after Confirm & cancel) =================
    dialog_title = '//android.view.View[@content-desc="Confirm cancel booking?"]'
    dialog_button_confirm = '//android.widget.Button[@content-desc="Confirm cancellation"]'
    dialog_button_go_back = '//android.widget.Button[@content-desc="Go back"]'
