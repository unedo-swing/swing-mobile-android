class CancelVerificationLocators:
    label_title = '//android.view.View[@content-desc="Cancel Swing Pass verification process?"]'
    label_description = ('//android.view.View[contains(@content-desc,'
                         '"Complete your Swing Pass verification")]')

    button_continue = '//android.widget.Button[@content-desc="Continue verification"]'
    button_later = '//android.widget.Button[@content-desc="Do verification later"]'

    scrim = '//android.view.View[@content-desc="Scrim"]'
