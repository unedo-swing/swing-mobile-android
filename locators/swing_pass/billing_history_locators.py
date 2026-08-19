class BillingHistoryLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Billing History"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # ================= rows =================
    # Every billing row. The price line is the one thing every row has, and the
    # currency prefix keeps the screen's clickable root out of the match.
    entry_any = '//android.view.View[@clickable="true" and contains(@content-desc,"Rp.")]'
    # the Nth row, 1-based and top-down — the list is newest first, so [1] is
    # the most recent charge
    entry_at = '(' + entry_any + ')[%d]'
    # a row by any fragment of its label — a date ("02 Aug 2026"), an amount
    # ("Rp. 150,000") or a period ("7 months")
    entry_by_text = '//android.view.View[@clickable="true" and contains(@content-desc,"%s")]'
