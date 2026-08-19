class CancelConfirmationLocators:
    # ================= copy =================
    # "You’ve saved Rp. 3,540,012. Are you sure you want to cancel?"
    label_title = '//android.view.View[contains(@content-desc,"Are you sure you want to cancel")]'
    # "You won’t be able to enjoy its exclusive rates and benefits anymore once it ends."
    label_warning = '//android.view.View[contains(@content-desc,"exclusive rates and benefits anymore")]'

    # ================= buttons =================
    button_stay = '//android.widget.Button[@content-desc="Stay with Swing Pass"]'
    button_proceed = '//android.widget.Button[@content-desc="Proceed to cancel"]'
    # the unlabelled button at the foot of the sheet (Close)
    button_close = '//android.widget.Button[not(@content-desc) or @content-desc=""]'
    # the dimmed area above the sheet; tapping it dismisses
    scrim = '//android.view.View[@content-desc="Scrim"]'
