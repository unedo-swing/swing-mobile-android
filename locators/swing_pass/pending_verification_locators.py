class PendingVerificationLocators:
    label_title = '//android.view.View[@content-desc="Waiting for your Swing Pass verification"]'
    label_description = ('//android.view.View[contains(@content-desc,'
                         '"Complete your Swing Pass verification")]')

    button_continue = '//android.widget.ImageView[@content-desc="Continue to verification"]'

    scrim = '//android.view.View[@content-desc="Scrim"]'
