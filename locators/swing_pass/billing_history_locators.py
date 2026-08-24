class BillingHistoryLocators:
    label_title = '//android.view.View[@content-desc="Billing History"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    entry_any = '//android.view.View[@clickable="true" and contains(@content-desc,"Rp.")]'
    entry_at = '(' + entry_any + ')[%d]'
    entry_by_text = '//android.view.View[@clickable="true" and contains(@content-desc,"%s")]'
