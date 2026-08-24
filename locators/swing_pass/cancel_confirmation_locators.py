class CancelConfirmationLocators:
    label_title = '//android.view.View[contains(@content-desc,"Are you sure you want to cancel")]'
    label_warning = '//android.view.View[contains(@content-desc,"exclusive rates and benefits anymore")]'

    button_stay = '//android.widget.Button[@content-desc="Stay with Swing Pass"]'
    button_proceed = '//android.widget.Button[@content-desc="Proceed to cancel"]'
    button_close = '//android.widget.Button[not(@content-desc) or @content-desc=""]'
    scrim = '//android.view.View[@content-desc="Scrim"]'
