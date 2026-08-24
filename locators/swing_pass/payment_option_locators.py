class PaymentOptionLocators:
    label_title = '//android.view.View[contains(@content-desc,"How would you like to pay")]'

    OPTION_RECURRING = "Recurring payment"
    OPTION_ONE_TIME = "One time payment"

    option_any = label_title + '/following-sibling::android.view.View[@clickable="true"]'
    option_by_name = '//android.view.View[@clickable="true" and starts-with(@content-desc,"%s")]'
    option_recurring = option_by_name % OPTION_RECURRING
    option_one_time = option_by_name % OPTION_ONE_TIME

    button_manual_transfer = '//android.widget.ImageView[@content-desc="Or manually transfer to us"]'

    button_close = '//android.widget.Button[not(@content-desc) or @content-desc=""]'
    scrim = '//android.view.View[@content-desc="Scrim"]'
