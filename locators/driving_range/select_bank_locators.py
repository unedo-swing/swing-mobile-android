"""
Android XPaths for the Swing > Select bank dialog.

Opened from Confirm cancellation > 'Select Bank'. A searchable list of banks for
the refund destination.

Flutter app — bank rows surface through ``content-desc``; the search field wraps
an EditText.
"""


class SelectBankLocators:
    label_title = '//android.view.View[@content-desc="Select bank"]'
    search_field = '//android.view.View[@content-desc="Search bank name"]'
    input_search = '//android.view.View[@content-desc="Search bank name"]//android.widget.EditText'
    # a bank row by its full name, e.g. "BPD Bali"
    bank_by_name = '//android.view.View[@content-desc="%s"]'
    # tap outside to dismiss
    scrim = '//android.view.View[@content-desc="Scrim"]'
